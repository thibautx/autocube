from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

landing_module = Blueprint('landing', __name__)

@landing_module.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('_garage.garage_home'))
    else:
        return render_template('index.html')
