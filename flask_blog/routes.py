import secrets
import os
from PIL import Image
from flask import render_template, redirect, url_for, flash, request, abort
from flask_blog import (
    app,
    bcrypt,
    db,
    mail,
    query_one_filtered,
    query_paginate_filtered,
    query_paginated,
)
from flask_blog.models import User, Post
from flask_blog.forms import (
    RegistrationForm,
    LoginForm,
    UpdateAccountForm,
    PostForm,
    RequestResetForm,
    ResetPasswordForm,
)
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message


@app.route("/")
@app.route("/home")
def home():
    page = request.args.get("page", 1, type=int)
    posts = query_paginated(Post, page)
    return render_template("home.html", posts=posts)


@app.route("/about")
def about():
    return render_template("about.html", title="About")


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(
            username=form.username.data, password=hashed_password, email=form.email.data
        )
        user.insert()
        flash(f"Account created for {form.username.data}. Login Here!", "success")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = query_one_filtered(User, email=form.email.data)

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("Login Unsuccessfull. Check email and password", "fail")
    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


def save_picture(picture_data):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(picture_data.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, "static/profile_pics", picture_fn)
    output_size = (125, 125)
    i = Image.open(picture_data)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_path = os.path.join(
                app.root_path, "static/profile_pics", current_user.image_file
            )
            if os.path.exists(picture_path):
                os.remove(picture_path)
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.update()
        flash("Your Account has been updated!", "success")
        return redirect(url_for("account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for("static", filename="profile_pics/" + current_user.image_file)
    return render_template(
        "account.html", title="Account", image_file=image_file, form=form
    )


@app.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data, content=form.content.data, author=current_user
        )
        post.insert()
        flash("Post has been created", "success")
        return redirect(url_for("home"))
    return render_template(
        "create_post.html", title="New Post", form=form, legend="New Post"
    )


@app.route("/post/<int:post_id>")
@login_required
def post(post_id):
    post = query_one_filtered(Post, id=post_id)
    if not post:
        abort(404)
    return render_template("post.html", title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    post = query_one_filtered(Post, id=post_id)
    if not post:
        abort(404)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.update()
        flash("Your Post has been updated ", "success")
        return redirect(url_for("post", post_id=post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template(
        "create_post.html", title="Update Post", form=form, legend="Update Post"
    )


@app.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = query_one_filtered(Post, id=post_id)
    if not post:
        abort(404)
    if post.author != current_user:
        abort(403)
    post.delete()
    flash("Your post has been deleted", "success")
    return redirect(url_for("home"))


@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get("page", 1, type=int)
    user = query_one_filtered(User, username=username)
    if not user:
        abort(404)
    posts = query_paginate_filtered(Post, page, author=user)
    return render_template("user_posts.html", posts=posts, title=username, user=user)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message(
        "Password Reset Request", sender="noreply@demo.com", recipients=[user.email]
    )
    msg.body = f"""To reset your password, visit the following link <h1>Hey there</h1>
{url_for('reset_token',token=token,_external=True)}

<p style="color: bisque;">If you did not make this request then simply ignore this email, no changes will be made</p>
"""
    mail.send(msg)


@app.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = query_one_filtered(User, email=form.email.data)
        if not user:
            flash(
                f"An email with your password reset link will be sent if {form.email.data} exists",
                "success",
            )
            return redirect(url_for("login"))
        send_reset_email(user)
        flash(
            f"An email with your password reset link will be sent if {form.email.data} exists",
            "success",
        )
        return redirect(url_for("login"))
    return render_template("reset_request.html", form=form, title="Reset Passord")


@app.route("/reset_password/<string:token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    user = User.verify_reset_token(token)
    if not user:
        flash("Invalid or Expired Token", "fail")
        return redirect(url_for("reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user.password = hashed_password
        user.update()
        flash(f"Password has been updated. Login Here!", "success")
        return redirect(url_for("login"))
    return render_template("reset_token.html", form=form, title="Rest Passord")
