import os
from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    request,
    abort,
    Blueprint,
    current_app,
)
from flask_blog.users.utils import save_picture, send_reset_email
from flask_blog import (
    bcrypt,
    query_one_filtered,
    query_paginate_filtered,
)
from flask_blog.models import User, Post
from flask_blog.users.forms import (
    RegistrationForm,
    LoginForm,
    UpdateAccountForm,
    RequestResetForm,
    ResetPasswordForm,
)
from flask_login import login_user, current_user, logout_user, login_required

users = Blueprint("users", __name__)


@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
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
        return redirect(url_for("users.login"))
    return render_template("register.html", title="Register", form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = query_one_filtered(User, email=form.email.data)

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("main.home"))
        else:
            flash("Login Unsuccessfull. Check email and password", "fail")
    return render_template("login.html", title="Login", form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_path = os.path.join(
                current_app.root_path, "static/profile_pics", current_user.image_file
            )
            if os.path.exists(picture_path):
                os.remove(picture_path)
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.update()
        flash("Your Account has been updated!", "success")
        return redirect(url_for("users.account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for("static", filename="profile_pics/" + current_user.image_file)
    return render_template(
        "account.html", title="Account", image_file=image_file, form=form
    )


@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get("page", 1, type=int)
    user = query_one_filtered(User, username=username)
    if not user:
        abort(404)
    posts = query_paginate_filtered(Post, page, author=user)
    return render_template("user_posts.html", posts=posts, title=username, user=user)


@users.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("users.home"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = query_one_filtered(User, email=form.email.data)
        if not user:
            flash(
                f"An email with your password reset link will be sent if {form.email.data} exists",
                "success",
            )
            return redirect(url_for("users.login"))
        send_reset_email(user)
        flash(
            f"An email with your password reset link will be sent if {form.email.data} exists",
            "success",
        )
        return redirect(url_for("users.login"))
    return render_template("reset_request.html", form=form, title="Reset Passord")


@users.route("/reset_password/<string:token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("users.home"))
    user = User.verify_reset_token(token)
    if not user:
        flash("Invalid or Expired Token", "fail")
        return redirect(url_for("users.reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user.password = hashed_password
        user.update()
        flash(f"Password has been updated. Login Here!", "success")
        return redirect(url_for("users.login"))
    return render_template("reset_token.html", form=form, title="Rest Passord")
