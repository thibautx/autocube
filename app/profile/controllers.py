from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import login_required, current_user, logout_user

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
        return redirect(url_for('.profile'))

@login_required
@profile_module.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('public.home'))