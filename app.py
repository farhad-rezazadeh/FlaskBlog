from flask import render_template

from config import app
from account.models import Post


@app.route("/")
def home():
    posts = Post.objects.all()
    return render_template("blog/home.html", posts=posts)


if __name__ == "__main__":
    app.run()
