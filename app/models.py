from flask_login import UserMixin

from app.instance import db


class User(UserMixin, db.Document):
    social_id = db.StringField(required=True)
    name = db.StringField(required=True)
    picture = db.StringField(required=True)
