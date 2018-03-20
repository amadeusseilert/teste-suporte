from bson import ObjectId
from bson.errors import InvalidId
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from mongoengine import DoesNotExist

from app.home.forms import NewPostForm
from app.models import Post, User, Guess

home_bp = Blueprint('home', __name__, template_folder='templates', url_prefix='/home')


@home_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = NewPostForm(request.form)
    posts = Post.objects.all()

    if form.validate_on_submit() and request.method == 'POST':
        author = User.objects(id=current_user.id).get()
        Post(text=form.text.data, truth=form.truth.data, author=author).save()
        return redirect(url_for('home.index'))

    return render_template('home.index.html', form=form, posts=posts)


@home_bp.route('/<post_id>/<guess>', methods=['POST'])
@login_required
def make_guess(post_id, guess):
    user = User.objects(id=current_user.id).get()

    try:
        post_id = ObjectId(post_id)
        post = Post.objects(id=post_id).get()
    except (TypeError, InvalidId, DoesNotExist):
        return redirect(url_for('home.index')), 400

    try:
        guess = bool(int(guess))
    except ValueError:
        return redirect(url_for('home.index')), 400

    Guess.guess_post(user, post, guess)
    return redirect(url_for('home.index'))

