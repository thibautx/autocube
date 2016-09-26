from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user
from app.profile.models import User
from app.garage.models import Car

appointments_module = Blueprint('_appointments', __name__, url_prefix='/appointments')

@login_required
@appointments_module.route('/')
def appointments():
    return render_template('appointments/index.html')

@login_required
@appointments_module.route('/appointments/schedule/<dealer_id>/<car_id>')
def schedule_with_dealer(dealer_id, car_id):
    car = Car.query.filter(Car.id == car_id)[0]
    dealer = User.query.filter(User.id == dealer_id)[0]
    return render_template('appointments/dealer_schedule.html',
                           dealer=dealer,
                           car=car)