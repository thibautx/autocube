from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app.profile.models import User

profile_module = Blueprint('_profile', __name__, url_prefix='/profile')


@login_required
@profile_module.route('/')
def profile():
    return render_template('profile/index.html')

@login_required
@profile_module.route('/update', methods=['POST'])
def update_profile():
    if request.method == 'POST':
        args = request.form.to_dict()
        for arg, value in args.items():
            setattr(current_user, arg, value)
        print current_user.__dict__
        return redirect(url_for('.profile'))