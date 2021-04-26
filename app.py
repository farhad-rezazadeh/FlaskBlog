from flask import render_template

from config import app


@app.route("/")
def home():
    return render_template("blog/home.html")


# Routs
from account import routes
from account.admin import routes


if __name__ == "__main__":
    app.run()
