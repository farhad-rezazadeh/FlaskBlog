from flask import render_template

from config import app
from account.models import Post


@app.route("/")
def home():
    posts = Post.objects.all()
    return render_template("blog/home.html", posts=posts)


@app.route("/<string:slug>")
def post_detail(slug):
    post = Post.objects.get_or_404(slug=slug)
    return render_template("blog/post_detail.html", post=post)


if __name__ == "__main__":
    app.run()
