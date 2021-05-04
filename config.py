import os

from dotenv import load_dotenv

from flask import Flask, render_template
from flask_bcrypt import Bcrypt
from authlib.integrations.flask_client import OAuth

# from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_mdeditor import MDEditor
from flask_mongoengine import MongoEngine
from flask_mail import Mail

# Load environment variable
load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = "bd232f0aca965d3284cc33812a6adc72"

# Database
app.config["MONGODB_SETTINGS"] = {"db": "user_login_system", "host": "127.0.0.1", "port": 27017}
db = MongoEngine(app)

# DebugToolbar
# toolbar = DebugToolbarExtension(app)

# Bcrypt for encrypt password
bcrypt = Bcrypt(app)

# Login Manager
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

# Email
app.config["MAIL_SERVER"] = "smtp.googlemail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
mail = Mail(app)

# oAuth Setup
oauth = OAuth(app)
google = oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    access_token_url="https://accounts.google.com/o/oauth2/token",
    access_token_params=None,
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    authorize_params=None,
    api_base_url="https://www.googleapis.com/oauth2/v1/",
    userinfo_endpoint="https://openidconnect.googleapis.com/v1/userinfo",
    client_kwargs={"scope": "openid email profile"},
)

# Flask-MDE
app.config["MDEDITOR_LANGUAGE"] = "en"
app.config["MDEDITOR_FILE_UPLOADER"] = os.path.join(
    app.root_path, "uploads"
)  # this floder uesd to save your uploaded image
mdeditor = MDEditor(app)

# Routs
from account import routes
