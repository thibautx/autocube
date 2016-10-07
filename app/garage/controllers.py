import json
import nhtsa
import edmunds
from app import db
from app.garage.models import Car
from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user
from app.profile.models import User
from pyzipcode import ZipCodeDatabase
from geopy.distance import vincenty

GOOGLE_MAPS_API_KEY = 'AIzaSyDC-_cXzQetjUnrB4GXyGyaK2qgLbwpkv4'
garage_module = Blueprint('_garage', __name__, url_prefix='/garage')

@garage_module.route('/')
@login_required
def garage_home():
    makes = edmunds.get_makes()
    cars = Car.query.filter(Car.user_id == current_user.id).all()
    return render_template('garage/index/garage.html',
                           cars=cars,
                           makes=json.dumps(makes))


@garage_module.route('/car/<id>')
def car_details(id):
    car = Car.query.get(id)
    return render_template('garage/car_details.html',
                           car=car,
                           recalls=car.recalls,
                           service_bulletins=car.service_bulletins,
                           maps_api=GOOGLE_MAPS_API_KEY)


@garage_module.route('/car/<id>/service', methods=['POST'])
def service_car(id):
    car = Car.query.get(id)
    zip = request.form['zip']
    try:
        max_distance = request.form['distance']
    except KeyError:
        pass

    # non registered dealers
    dealers = edmunds.get_dealers(zip, car.make)

    autocube_dealers = User.query.filter(User.is_service == True and _distance_filter(User.zip, zip) == True).all()
    # import pprint
    # pp = pprint.PrettyPrinter(indent=2)
    # pp.pprint(dealers[0])
    return render_template('garage/service_car.html',
                           autocube_dealers=autocube_dealers,
                           dealers=dealers,
                           car=car)


def _distance_filter(dealer_zip, customer_zip, max_distance=10):
    zcdb = ZipCodeDatabase()
    dealer_lat_long = (zcdb[dealer_zip].latitude, zcdb[dealer_zip].longitude)
    customer_lat_long = (zcdb[customer_zip].latitude, zcdb[customer_zip].longitude)
    distance = vincenty(dealer_lat_long, customer_lat_long)
    print distance
    return distance < max_distance


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
        return redirect(url_for('.garage_home'))


@garage_module.route('/car/delete/<int:id>', methods=['POST'])
def remove_car(id):
    if request.method == 'POST':
        db.session.delete(Car.query.get(id))
        db.session.commit()
        return redirect(url_for('.garage_home'))


@garage_module.route('/car/update/<int:id>', methods=['POST'])
def update_car(id):
    if request.method == 'POST':
        car = Car.query.get(id)
        args = request.form.to_dict()
        for arg, value in args.items():
            setattr(car, arg, value)
        db.session.commit()
        return redirect(url_for('.car_details', id=id))


@garage_module.route('/models', methods=['GET'])
def models():
    if request.method == 'GET':
        make = request.args.get('make')
        models = edmunds.get_models(make)
        return json.dumps(models)


@garage_module.route('/model-years', methods=['GET'])
def model_years():
    if request.method == 'GET':
        make = request.args.get('make')
        model = request.args.get('model')
        _model_years = edmunds.get_model_years(make, model)
        return json.dumps(_model_years)


# TODO: http://0.0.0.0:5000/garage/car error handler
@garage_module.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('.garage_home'))
# @recalls_module.route('/filter', methods=['GET', 'POST'])
# def filter():
#     if request.method == 'GET':
#         year = request.args.get('year')
#         make = request.args.get('make')
#         model = request.args.get('model')
#         garage = nhtsa.get_recalls(year, make, model)
#         dealers = edmunds.get_dealers(60601, make)
#         return render_template('garage/index.html', garage=garage, dealers=dealers)
