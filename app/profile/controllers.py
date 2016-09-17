from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.profile.models import User

profile_module = Blueprint('_profile', __name__, url_prefix='/profile')


@profile_module.route("/")
@login_required
def profile():
    user = User.query.get(current_user.id)
    return render_template('profile/index.html', user=user)

