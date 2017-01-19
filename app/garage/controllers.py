import json

from utils import on_new_car

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

import edmunds
from app import db
from app.garage.models import Car

GOOGLE_MAPS_API_KEY = 'AIzaSyDC-_cXzQetjUnrB4GXyGyaK2qgLbwpkv4'
garage_module = Blueprint('_garage', __name__, url_prefix='/garage')


@garage_module.route('/')
@login_required
def garage_home():
    """
    Home page for a garage

    :return:
    """
    makes = edmunds.get_makes()
    cars = Car.query.filter(Car.user_id == current_user.id).all()
    return render_template('garage/garage.html',
                           cars=cars,
                           makes=json.dumps(makes))


@garage_module.route('/car/<car_id>')
@login_required
def car_details(car_id):
    """
    View details of specific car.

    :param car_id: (int) car id
    :return:
    """
    car = Car.query.get(car_id)

    # if current user doesn't own the car, then redirect to garage home
    try:
        if car.user_id != current_user.id:
            return redirect(url_for('.garage_home'))
    except AttributeError:
        return redirect(url_for('.garage_home'))

    return render_template('garage/car_details/car_details.html',
                           car=car,
                           recalls=car.recalls,
                           service_bulletins=car.service_bulletins,
                           maps_api=GOOGLE_MAPS_API_KEY)


# API
@garage_module.route('/car', methods=['POST'])
@login_required
def add_car():
    if request.method == 'POST':
        make = request.form['make']
        model = request.form['model']
        year = request.form['year']
        car = Car(make=make,
                  model=model,
                  year=year,
                  user_id=current_user.id)
        db.session.add(car)
        db.session.commit()

        on_new_car(car)

        # if car doesn't exist already in database, update recalls/service bulletins
        # if len(Car.query.filter(Car.make == make and Car.model == model and Car.year == year).all()) == 0:
        #     update_recalls()
        #     update_service_bulletins()

        return redirect(url_for('.garage_home'))


@garage_module.route('/car/delete/<car_id>', methods=['POST'])
def remove_car(car_id):
    """
    Remove car from database.

    :param car_id:
    :return:
    """
    if request.method == 'POST':
        db.session.delete(Car.query.get(car_id))
        db.session.commit()
        return redirect(url_for('.garage_home'))


@garage_module.route('/car/update/<car_id>', methods=['POST'])
def update_car(car_id):
    """
    Update car info.

    :param car_id:
    :return:
    """
    if request.method == 'POST':
        car = Car.query.get(car_id)
        args = request.form.to_dict()
        for arg, value in args.items():
            setattr(car, arg, value)
        db.session.commit()
        return redirect(url_for('.car_details', id=car_id))


@garage_module.route('/models', methods=['GET'])
def get_models():
    """
    Get all possible models from edmunds.

    :return:
    """
    if request.method == 'GET':
        make = request.args.get('make')
        models = edmunds.get_models(make)
        return json.dumps(models)


@garage_module.route('/model-years', methods=['GET'])
def model_years():
    """
    Get all possible years for a make/model combination from Edmunds.

    :return:
    """
    if request.method == 'GET':
        make = request.args.get('make')
        model = request.args.get('model')
        _model_years = edmunds.get_model_years(make, model)
        return json.dumps(_model_years)
