from flask import Blueprint, render_template
from flask_login import login_required

profile_module = Blueprint('_profile', __name__, url_prefix='/profile')


@profile_module.route("/")
@login_required
def profile():
    return render_template('profile/index.html')

