from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . import db

main = Blueprint('main', __name__)

# homepage
@main.route('/')
def index():
    return render_template('index.html')

# profile page
@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)