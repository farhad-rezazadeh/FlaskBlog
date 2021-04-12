from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from markupsafe import Markup


class RegistrationForm(FlaskForm):
    username_markup = Markup('<i class="zmdi zmdi-account material-icons-name"></i>')
    email_markup = Markup('<i class="zmdi zmdi-email"></i>')
    password_markup = Markup('<i class="zmdi zmdi-lock"></i>')
    confirm_password_markup = Markup('<i class="zmdi zmdi-lock-outline"></i>')

    username = StringField(username_markup, validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField(email_markup, validators=[DataRequired(), Email()])
    password = PasswordField(password_markup, validators=[DataRequired()])
    confirm_password = PasswordField(confirm_password_markup, validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Sign Up")


class LoginForm(FlaskForm):
    email_markup = Markup('<i class="zmdi zmdi-email"></i>')
    password_markup = Markup('<i class="zmdi zmdi-lock"></i>')
    submit_markup = Markup("<span><span></span></span>Remember me")

    email = StringField(email_markup, validators=[DataRequired(), Email()])
    password = PasswordField(password_markup, validators=[DataRequired()])
    remember = BooleanField(submit_markup)
    submit = SubmitField("Log In")
