from flask import render_template

from config import app


@app.route("/")
def home():
    return render_template("blog/home.html")


if __name__ == "__main__":
    app.run()
