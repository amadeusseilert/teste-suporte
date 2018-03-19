import jinja2
from flask import Flask
from flask_login import LoginManager
from flask_mongoengine import MongoEngine
from mongoengine import DoesNotExist

db = MongoEngine()
lm = LoginManager()
lm.login_view = 'auth.index'


@lm.user_loader
def load_user(user_id):
    from app.models import User
    try:
        return User.objects(id=user_id).get()
    except DoesNotExist:
        return None


def create_app(config):
    app = UserShareApp()
    app.config.from_object(config)
    db.init_app(app)
    lm.init_app(app)

    from app.oauth.views import auth_bp
    app.register_blueprint(auth_bp)

    from app.home.views import home_bp
    app.register_blueprint(home_bp)

    return app


class UserShareApp(Flask):
    def __init__(self):
        Flask.__init__(self, __name__)

        self.jinja_loader = jinja2.ChoiceLoader([
            self.jinja_loader,
            jinja2.PrefixLoader({}, delimiter=".")
        ])

    def create_global_jinja_loader(self):
        return self.jinja_loader

    def register_blueprint(self, bp):
        Flask.register_blueprint(self, bp)
        self.jinja_loader.loaders[1].mapping[bp.name] = bp.jinja_loader
