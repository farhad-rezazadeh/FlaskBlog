from flask_login import UserMixin

from app import db


# Define the User document.
# NB: Make sure to add flask_user UserMixin !!!
class User(UserMixin, db.Document):
    meta = {"collection": "users"}
    active = db.BooleanField(default=True)

    # User authentication information
    email = db.EmailField()
    password = db.StringField()

    # User information
    username = db.StringField(default="")

    # Relationships
    posts = db.ListField(db.StringField(), default=[])
