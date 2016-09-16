from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user

appointments_module = Blueprint('_appointments', __name__, url_prefix='/appointments')

@login_required
@appointments_module.route('/')
def appointments():
    return render_template('appointments/index.html')