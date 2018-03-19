from flask import Blueprint, render_template
from flask_login import login_required

home_bp = Blueprint('home', __name__, template_folder='templates', url_prefix='/home')


@home_bp.route('/')
@login_required
def index():
    return render_template('home.index.html')
