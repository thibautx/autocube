from flask import Blueprint, render_template
from flask_login import login_required

appointments_module = Blueprint('_appointments', __name__, url_prefix='/appointments')

@login_required
@appointments_module.route('/')
def appointments():
    return render_template('appointments/index.html')

