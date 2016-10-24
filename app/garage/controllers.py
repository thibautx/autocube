import json

from update_database import update_recalls, update_service_bulletins

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


@garage_module.route('/car/<id>')
@login_required
def car_details(id):
    """
    View details of specific car.

    :param id: (int) car id
    :return:
    """
    car = Car.query.get(id)

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


# API Methods
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

        # if car doesn't exist already in database, update recalls/service bulletins
        if len(Car.query.filter(Car.make == make and Car.model == model and Car.year == year).all()) == 0:
            update_recalls()
            update_service_bulletins()

        return redirect(url_for('.garage_home'))


@garage_module.route('/car/delete/<int:id>', methods=['POST'])
def remove_car(id):
    """
    Remove car from database.

    :param id:
    :return:
    """
    if request.method == 'POST':
        db.session.delete(Car.query.get(id))
        db.session.commit()
        return redirect(url_for('.garage_home'))


@garage_module.route('/car/update/<int:id>', methods=['POST'])
def update_car(id):
    """
    Update car info.

    :param id:
    :return:
    """
    if request.method == 'POST':
        car = Car.query.get(id)
        args = request.form.to_dict()
        for arg, value in args.items():
            setattr(car, arg, value)
        db.session.commit()
        return redirect(url_for('.car_details', id=id))


@garage_module.route('/models', methods=['GET'])
def models():
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