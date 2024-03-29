from flask import Blueprint
from flask import render_template, request
from flask_blog import query_paginated, query_all_filtered
from flask_blog.models import Post, Comment


main = Blueprint("main", __name__)

@main.route("/home")
@main.route("/")
def home():
    page = request.args.get("page", 1, type=int)
    posts = query_paginated(Post, page)
    return render_template("home.html", posts=posts)


@main.route("/about")
def about():
    return render_template("about.html", title="About")
