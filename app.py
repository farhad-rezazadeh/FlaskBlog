import os

from flask import Flask, render_template, flash, redirect, url_for
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "bd232f0aca965d3284cc33812a6adc72"


@app.route("/")
def home():
    return render_template("blog/home.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}!", category="success")
        return redirect(url_for("home"))
    return render_template("account/register.html", title="Register", form=form)


@app.route("/login")
def login():
    form = LoginForm()
    return render_template("account/login.html", title="Login", form=form)


if __name__ == "__main__":
    app.run()
