import datetime

from bson import Code
from flask_login import UserMixin

from app.instance import db


class User(UserMixin, db.Document):
    social_id = db.StringField(required=True)
    name = db.StringField(required=True)
    picture = db.StringField(required=True)

    SCORE_MAP = Code('function(){emit(this.id, [this.post.right_guesses_share, this.post.wrong_guesses_share]);}')
    SCORE_REDUCE = Code('function(key, values){return [Array.sum(values[0]), Array.sum(values[1])];}')

    @property
    def score(self):
        author_score = Post.objects(author=self).sum('author_score')
        guesses = Guess.objects(user=self).only('post')
        right_guesses_score = sum(g.post.right_guess_share for g in guesses)
        wrong_guesses_score = sum(g.post.wrong_guess_share for g in guesses)
        return '{:.2f}'.format(author_score + right_guesses_score - wrong_guesses_score)


class Post(db.Document):
    text = db.StringField(required=True)
    date = db.DateTimeField(default=datetime.datetime.now())
    truth = db.BooleanField(required=True)
    author = db.ReferenceField(User)
    true_guesses = db.IntField(default=0)
    false_guesses = db.IntField(default=0)

    author_score = db.FloatField(default=0.0)
    right_guess_share = db.FloatField(default=0.0)
    wrong_guess_share = db.FloatField(default=0.0)

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
    def update_score(cls, post):
        total_author = 0.0
        # Right guesses
        guesses = cls.objects(post=post, guess=post.truth)
        guesses_count = guesses.count()
        if guesses_count > cls.MINIMUM_COUNT:
            amount = cls.SCALE_FACTOR * guesses_count - cls.MINIMUM_COUNT
            total_author -= amount
            post.right_guess_share = amount / guesses_count

        # Wrong guesses
        guesses = cls.objects(post=post, guess=(not post.truth))
        guesses_count = guesses.count()
        if guesses_count > cls.MINIMUM_COUNT:
            amount = cls.SCALE_FACTOR * guesses_count - cls.MINIMUM_COUNT
            total_author += amount
            post.wrong_guess_share = amount / guesses_count

        post.author_score = total_author
        post.save()

    @classmethod
    def guess_post(cls, user, post, guess):
        # Save the new guess
        cls(user=user, post=post, guess=guess).save()
        if guess is True:
            post.true_guesses += 1
            post.save()
        else:
            post.false_guesses += 1
            post.save()
        # Update guesses score
        cls.update_score(post)
