import datetime

from flask_login import UserMixin

from app.instance import db


class User(UserMixin, db.Document):
    social_id = db.StringField(required=True)
    name = db.StringField(required=True)
    picture = db.StringField(required=True)
    score = db.FloatField(default=0.0)


class Post(db.Document):
    text = db.StringField(required=True)
    date = db.DateTimeField(default=datetime.datetime.now())
    truth = db.BooleanField(required=True)
    author = db.ReferenceField(User)

    @property
    def time_delta(self):
        delta = datetime.datetime.now() - self.date
        if delta.days > 1:
            return '{} days ago.'.format(delta.days)
        elif delta.days == 1:
            return '1 day ago.'
        elif delta.seconds >= 7200:
            return '{} hours ago.'.format(delta.seconds // 3600)
        elif delta.seconds >= 3600:
            return '1 hour ago.'
        elif delta.seconds >= 120:
            return '{} minutes ago.'.format(delta.seconds // 60)
        elif delta.seconds >= 60:
            return '1 minute ago.'
        else:
            return 'Just now.'

    def already_guessed(self, user):
        ag = Guess.objects(user=user, post=self).first()
        if ag:
            return True
        else:
            return False


class Guess(db.Document):

    MINIMUM_COUNT = 2
    SCALE_FACTOR = 2.0

    user = db.ReferenceField(User)
    post = db.ReferenceField(Post)
    guess = db.BooleanField(required=True)

    @classmethod
    def update_score(cls, amount, post, guesses):
        author = post.author
        author.score -= amount
        share = len(guesses) / amount
        for guesser in (g.user for g in guesses):
            guesser.score += share

    @classmethod
    def guess_post(cls, user, post, guess):
        # Save the new guess

        cls(user=user, post=post, guess=bool(int(guess))).save()

        # Update right guesses score
        guesses = cls.objects(post=post, guess=post.truth)
        amount = cls.SCALE_FACTOR * (len(guesses) - cls.MINIMUM_COUNT)
        if len(guesses) > cls.MINIMUM_COUNT:
            cls.update_score(amount, post, guesses)

        # Update wrong guesses score
        guesses = cls.objects(post=post, guess=(not post.truth))
        amount = cls.SCALE_FACTOR * (len(guesses) - cls.MINIMUM_COUNT)
        if len(guesses) > cls.MINIMUM_COUNT:
            cls.update_score(amount, post, guesses)
