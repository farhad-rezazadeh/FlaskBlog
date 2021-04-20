from flask import Flask, render_template
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface
from flask_debugtoolbar import DebugToolbarExtension
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config["SECRET_KEY"] = "bd232f0aca965d3284cc33812a6adc72"

# Database
app.config["MONGODB_SETTINGS"] = {"db": "user_login_system", "host": "127.0.0.1", "port": 27017}
db = MongoEngine(app)
# app.session_interface = MongoEngineSessionInterface(db)
# toolbar = DebugToolbarExtension(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"


@login_manager.user_loader
def load_user(user_id):
    return User.objects.get(id=user_id)


# Routs
from account.routes import *


@app.route("/")
def home():
    return render_template("blog/home.html")


if __name__ == "__main__":
    app.run()
