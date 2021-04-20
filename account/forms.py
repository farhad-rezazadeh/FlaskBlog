from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from markupsafe import Markup

from account.models import User


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
