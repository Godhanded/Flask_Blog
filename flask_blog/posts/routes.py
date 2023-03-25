from flask import render_template, redirect, url_for, flash, request, abort, Blueprint
from flask_blog import query_one_filtered, query_all_filtered,db
from flask_blog.models import Post, Comment,Like
from flask_blog.posts.forms import PostForm, CommentForm
from flask_login import current_user, login_required


posts = Blueprint("posts", __name__)


@posts.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data, content=form.content.data, author=current_user
        )
        post.insert()
        flash("Post has been created", "success")
        return redirect(url_for("main.home"))
    return render_template(
        "create_post.html", title="New Post", form=form, legend="New Post"
    )


@posts.route("/post/<int:post_id>")
@login_required
def post(post_id):
    form = CommentForm()
    post = query_one_filtered(Post, id=post_id)
    if not post:
        abort(404)
    comments = query_all_filtered(Comment, post_id=post.id)
    return render_template(
        "post.html", title=post.title, post=post, form=form, comments=comments
    )

@posts.route("/post/<int:post_id>/like",methods=["POST"])
@login_required
def like_post(post_id):
    like = db.session.execute(db.select(Like).filter_by(post_id=post_id).filter_by(user=current_user)).scalar_one_or_none()
    if not like:
        like = Like(None,current_user,post_id)
        like.insert()
    else:
        like.delete()
    return redirect(request.referrer)

@posts.route("/post/comment/<int:comment_id>/like",methods=["POST"])
@login_required
def like_comment(comment_id):
    like = db.session.execute(db.select(Like).filter_by(comment_id=comment_id).filter_by(user=current_user)).scalar_one_or_none()
    if not like:
        like = Like(comment_id,current_user,None)
        like.insert() 
    else:
        like.delete()
    return redirect(request.referrer)


@posts.route("/post/<int:post_id>/update", methods=["GET", "POST"])
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
        return redirect(url_for("posts.post", post_id=post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template(
        "create_post.html", title="Update Post", form=form, legend="Update Post"
    )


@posts.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = query_one_filtered(Post, id=post_id)
    if not post:
        abort(404)
    if post.author != current_user:
        abort(403)
    post.delete()
    flash("Your post has been deleted", "success")
    return redirect(url_for("main.home"))


@posts.route("/post/<int:post_id>/comment", methods=["POST"])
@login_required
def send_comment(post_id):
    form = CommentForm(request.form)
    if form.validate_on_submit():
        comment = Comment(form.comment.data, current_user, post_id)
        comment.insert()
        return redirect(url_for("posts.post", post_id=post_id))


@posts.route("/post/<int:comment_id>/delcomment", methods=["POST"])
@login_required
def delete_comment(comment_id):
    comment = query_one_filtered(Comment, id=comment_id)
    if not comment:
        abort(404)
    comment.delete()
    return redirect(request.referrer)
