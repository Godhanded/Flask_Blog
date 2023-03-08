from flask import render_template, redirect, url_for, flash,request
from flask_blog import app, bcrypt, db, query_one_filtered, query_all_filtered
from flask_blog.models import User, Post
from flask_blog.forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user,login_required


posts = [
    {
        "author": "Corey Schafer",
        "title": "Blog Post 1",
        "content": "First post content",
        "date_posted": "April 20, 2018",
    },
    {
        "author": "Jane Doe",
        "title": "Blog Post 2",
        "content": "Second post content",
        "date_posted": "April 21, 2018",
    },
]


@app.route("/")
@app.route("/home")
def home():
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
        flash(f"Account created for {form.username.data}. Login Here!", "bg-green-400")
        return redirect(url_for("login"))
    print(form.form_errors)
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
            next_page=request.args.get('next')
            print(next_page)
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("Login Unsuccessfull. Check email and password", "bg-rose-400")
    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/account")
@login_required
def account():
    return render_template("account.html", title="Account")
