import uuid

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin

from config import app, db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.objects.get(id=user_id)


# Define the User document.
# NB: Make sure to add flask_user UserMixin !!!
class User(UserMixin, db.Document):
    meta = {"collection": "users"}
    id = db.StringField(default=lambda: str(uuid.uuid4()), primary_key=True)

    active = db.BooleanField(default=True)

    # User authentication information
    email = db.EmailField()
    password = db.StringField()

    # User information
    username = db.StringField(default="")

    # User image
    image = db.StringField(default="default.jpg")

    # Relationships
    posts = db.ListField(db.StringField(), default=[])

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config["SECRET_KEY"], expires_sec)
        return s.dumps({"user_id": self.id}).decode("utf-8")

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token)["user_id"]
        except:
            return None
        return User.objects.get(id=user_id)
