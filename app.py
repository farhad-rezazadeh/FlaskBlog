from flask import render_template, request

from config import app
from account.models import Post, User


@app.route("/")
def home():
    page = request.args.get("page", 1, type=int)
    posts = Post.objects.paginate(page=page, per_page=3)
    return render_template("blog/home.html", posts=posts)


@app.route("/<string:slug>")
def post_detail(slug):
    post = Post.objects.get_or_404(slug=slug)
    return render_template("blog/post_detail.html", post=post)


@app.route("/posts/<string:username>")
def post_of_author(username):
    author = User.objects.get_or_404(username=username)
    page = request.args.get("page", 1, type=int)
    posts = Post.objects.filter(author=author).paginate(page=page, per_page=3)
    return render_template("blog/home.html", posts=posts)


if __name__ == "__main__":
    app.run()
