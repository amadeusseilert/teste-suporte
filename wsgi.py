import datetime

from app.instance import create_app
from app.models import Guess
from config import DevelopmentConfig


def populate_database(app):
    with app.app_context():
        from app.models import User, Post

        User.drop_collection()
        Post.drop_collection()
        Guess.drop_collection()

        superman = User(social_id='123', name='Clark Kent', picture='//').save()
        batman = User(social_id='122', name='Bruce Banner', picture='//').save()
        wwoman = User(social_id='321', name='Diana Prince', picture='//').save()

        now = datetime.datetime.now()
        p1 = Post(text='I am poor.', date=now, truth=False, author=batman).save()
        Post(text='I can beat the Superman.', date=now, truth=True, author=batman).save()
        Post(text='I have no weakness.', date=now, truth=False, author=superman).save()
        Post(text='I am an Amazonian', date=now, truth=True, author=wwoman).save()
        Post(text='My car is visible.', date=now, truth=False, author=wwoman).save()

        Guess(user=superman, post=p1, guess=False).save()
        Guess(user=wwoman, post=p1, guess=False).save()


if __name__ == '__main__':
    app = create_app(DevelopmentConfig)
    import sys
    if '--init-db' in sys.argv:
        populate_database(app)
    else:
        app.run()
