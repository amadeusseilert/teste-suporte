from flask import redirect, url_for, render_template, flash, Blueprint
from flask_login import login_user, logout_user, current_user
from app.oauth.auth import OAuthSignIn


auth_bp = Blueprint('auth', __name__, template_folder='templates')


@auth_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('home.index'))
    return render_template('auth.index.html')


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.index'))


@auth_bp.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('auth.index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@auth_bp.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('auth.index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, name, picture = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('auth.index'))

    from app.models import User
    user = User.objects(social_id=social_id).first()
    if not user:
        user = User(social_id=social_id, name=name, picture=picture).save()
    login_user(user, True)
    return redirect(url_for('auth.index'))
