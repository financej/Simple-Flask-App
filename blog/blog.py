from flask import Blueprint, abort, render_template, redirect, request, url_for
from slugify import slugify

from .db import Post, db


bp = Blueprint("blog", __name__, url_prefix="/")


# 데이터베이스를 쿼리하여 날짜별로 내림차순으로 반환
def get_posts():
    """
    Return all of the posts a given user created, ordered by date.
    """
    return Post.query.order_by(Post.created.desc())


@bp.route("/")
def index():
    """
    Render the homepage.
    """
    posts = Post.query.order_by(Post.created.desc())
    posts_final = []

    for post in posts:
        posts_final.append(post)

    return render_template("blog/index.html", posts=posts_final)


@bp.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    """
    Render the dashboard page.
    """
    if request.method == "GET":
        return render_template("blog/dashboard.html", posts=get_posts())

    post = Post(
        title=request.form.get("title"),
        body=request.form.get("body"),
        slug=slugify(request.form.get("title"))
    )

    db.session.add(post)
    db.session.commit()

    return render_template("blog/dashboard.html", posts=get_posts())


# SLUG 기능은 유효한 URL 을 생성하는 방법(노션 참고)
# URL 에 SLUG 가 지정된 블로그 게시물에 대한 데이터베이스를 찾습니다.
# 하나를 찾을 수 있으면 해당 페이지를 렌더링하고 사용자에게 블로그를 표시합니다
@bp.route("/<slug>")
def view_post(slug):
    """View a post."""
    post = Post.query.filter_by(slug=slug).first()
    if not post:
        abort(404)

    return render_template("blog/post.html", post=post)


@bp.route("/<slug>/edit", methods=["GET", "POST"])
def edit_post(slug):
    """Edit a post."""
    post = Post.query.filter_by(slug=slug).first()

    if not post:
        abort(404)

    if request.method == "GET":
        return render_template("blog/edit.html", post=post)

    post.title = request.form.get("title")
    post.body = request.form.get("body")
    post.slug = slugify(request.form.get("title"))

    db.session.commit()
    return redirect(url_for(".view_post", slug=post.slug))


@bp.route("/<slug>/delete", methods=["POST"])
def delete_post(slug):
    """Delete a post."""
    post = Post.query.filter_by(slug=slug).first()

    if not post:
        abort(404)

    db.session.delete(post)
    db.session.commit()

    return redirect(url_for(".dashboard"))
