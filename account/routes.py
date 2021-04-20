from flask import render_template, flash, redirect, url_for
from flask_login import login_user, current_user, logout_user, login_required

from app import app, bcrypt
from account.models import User
from account.forms import RegistrationForm, LoginForm


@app.route("/account/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(email=form.email.data, username=form.username.data, password=hashed_password).save()
        login_user(user)
        flash(f"Account created for {form.username.data}!", category="success")
        return redirect(url_for("home"))
    return render_template("account/register.html", title="Register", form=form)


@app.route("/account/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects.get_or_404(email=form.email.data)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash("You have been logged in!", "success")
            return redirect(url_for("home"))
        else:
            flash("Login unsuccessful", "danger")
    return render_template("account/login.html", title="Login", form=form)


@app.route("/account/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))
