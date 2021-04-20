from flask_login import UserMixin

from config import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.objects.get(id=user_id)


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
