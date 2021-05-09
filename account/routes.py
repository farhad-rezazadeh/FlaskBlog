import os
import secrets
from PIL import Image

from flask import render_template, flash, redirect, url_for, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

from config import app, bcrypt, mail, oauth
from account.models import User, Post
from account.forms import (
    RegistrationForm,
    LoginForm,
    RequestResetForm,
    ResetPasswordForm,
    UpdateAccountForm,
    PostForm,
    UpdatePostForm,
)


@app.route("/account/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(email=form.email.data, username=form.username.data, password=hashed_password).save()
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
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("Login unsuccessful", "danger")
    return render_template("account/login.html", title="Login", form=form)


@app.route("/account/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message("Password Reset Request", sender="noreply@demo.com", recipients=[user.email])
    msg.body = f"""To reset Your password,Visit the following link:
    {url_for('reset_request', _external=True)}/{token}
    if you did not make this email request simply ignore this email.
    """
    mail.send(msg)


@app.route("/account/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.objects.filter(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent with instructions to reset your password", "info")
        return redirect(url_for("login"))
    return render_template("account/reset_request.html", title="Reset Password", form=form)


@app.route("/account/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    user = User.verify_reset_token(token)
    if user is None:
        flash("That is an invalid or expired token", "warning")
        return redirect(url_for("reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user.password = hashed_password
        user.save()
        flash(f"Your password has been update!", category="success")
        return redirect(url_for("home"))
    return render_template("account/reset_token.html", title="Reset Password", form=form)


@app.route("/google_login")
def google_login():
    google = oauth.create_client("google")  # create the google oauth client
    redirect_uri = url_for("authorize", _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route("/authorize")
def authorize():
    google = oauth.create_client("google")  # create the google oauth client
    token = google.authorize_access_token()  # Access token from google (needed to get user info)
    resp = google.get("userinfo")  # userinfo contains stuff u specificed in the scrope
    user_info = resp.json()
    user = oauth.google.userinfo()  # uses openid endpoint to fetch user info
    # Here you use the profile/user data that you got and query your database find/register the user
    # and set ur own data in the session not the profile from google
    user = User.objects.filter(email=user.email).first()
    if user:
        login_user(user, remember=False)
        flash("You have been logged in!", "success")
        next_page = request.args.get("next")
        return redirect(next_page) if next_page else redirect(url_for("home"))
    else:
        flash("Login unsuccessful", "danger")
    return redirect(url_for("login"))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, "static/profile_pics", picture_fn)

    output_size = (150, 150)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        user = User.objects.filter(email=current_user.email).first()
        user.username = form.username.data
        user.email = form.email.data
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            user.image = picture_file
        user.save()
        flash("your account has been updated!", "success")
        return redirect(url_for("profile"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for("static", filename=f"profile_pics/{current_user.image}")
    return render_template("account/adminlte/profile.html", title="Account", image_file=image_file, form=form)


@app.route("/account/article/new", methods=["GET", "POST"])
@login_required
def new_article():
    form = PostForm()
    if form.validate_on_submit():
        user = User.objects.get_or_404(id=current_user.id)
        post = Post(title=form.title.data, content=form.content.data, slug=form.slug.data, author=user).save()
        flash("Your post has been created!", "success")
        return redirect(url_for("new_article"))
    return render_template("account/adminlte/create_article.html", title="New Article", form=form)


@app.route("/account/article/update/<string:slug>", methods=["GET", "POST"])
@login_required
def update_article(slug):
    post = Post.objects.get_or_404(slug=slug)
    if post.author != current_user:
        abort(403)
    form = UpdatePostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.save()
        flash("Your post has been updated!", "success")
        return redirect(url_for("home"))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template("account/adminlte/update_article.html", title="Update Post", form=form)
