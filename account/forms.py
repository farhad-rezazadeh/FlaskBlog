from flask_mdeditor import MDEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from markupsafe import Markup

from account.models import User, Post


class RegistrationForm(FlaskForm):
    username = StringField(validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField(validators=[DataRequired(), Email()])
    password = PasswordField(validators=[DataRequired()])
    confirm_password = PasswordField(validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Sign Up")

    def validate_email(self, field):
        try:
            User.objects.get(email=field.data)
        except:
            pass
        else:
            raise ValidationError("There is already account with this Email!")

    def validate_username(self, username):
        user = User.objects.filter(username=username.data).first()
        if user:
            raise ValidationError("That username is taken. Please choose a different one.")


class LoginForm(FlaskForm):
    remember_markup = Markup('<span class="caption">Remember me</span>')

    email = StringField(validators=[DataRequired(), Email()])
    password = PasswordField(validators=[DataRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField("Log In")

    def validate_email(self, field):
        try:
            User.objects.get(email=field.data)
        except:
            raise ValidationError("There is not account with this Email!")


class RequestResetForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email()])
    submit = SubmitField("Request Password Reset")

    def validate_email(self, field):
        user = User.objects.filter(email=field.data).first()
        if user is None:
            raise ValidationError("There is no account with that Email!!")


class ResetPasswordForm(FlaskForm):
    password = PasswordField(validators=[DataRequired()])
    confirm_password = PasswordField(validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Reset Password")


class UpdateAccountForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    picture = FileField("Update Profile Picture", validators=[FileAllowed(["jpg", "png"])])
    submit = SubmitField("Update")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.objects.filter(username=username.data).first()
            if user:
                raise ValidationError("That username is taken. Please choose a different one.")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.objects.filter(email=email.data).first()
            if user:
                raise ValidationError("That email is taken. Please choose a different one.")


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    slug = StringField("Slug", validators=[DataRequired()])
    content = MDEditorField("Content", validators=[DataRequired()])

    submit = SubmitField("Post")

    def validate_slug(self, slug):
        post = Post.objects.filter(slug=slug.data).first()
        if post:
            raise ValidationError("That Slug is taken. Please choose a different one.")
