import json
from geopy.distance import vincenty
from pyzipcode import ZipCodeDatabase
from app.garage import edmunds
from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from app.service.models import Dealer
from app.garage.models import Car

service_module = Blueprint('_service', __name__, url_prefix='/service')

@service_module.route('/')
def home():
    makes = edmunds.get_makes()
    return render_template("service/index.html",
                           makes=json.dumps(makes))

@service_module.route('/dealers', methods=['GET'])
def list_dealers():
    if request.method == 'GET':
        makes = json.dumps(edmunds.get_makes())

        make = request.args['make']
        zip = request.args['zip']
        dealers = []
        return render_template("service/index.html",
                               makes=makes,
                               dealers=dealers)

@service_module.route('/car/<id>/service', methods=['POST'])
def service_car(id):
    car = Car.query.get(id)
    zip = request.form['zip']
    try:
        max_distance = request.form['distance']
    except KeyError:
        pass

    # non registered dealers
    dealers = edmunds.get_dealers(zip, car.make)
    autocube_dealers = Dealer.query.filter(_distance_filter(Dealer.zip, zip) == True).all()
    # import pprint
    # pp = pprint.PrettyPrinter(indent=2)
    # pp.pprint(dealers[0])
    return render_template('service/list_dealers.html',
                           autocube_dealers=autocube_dealers,
                           dealers=dealers,
                           car=car)

@service_module.route('/fix-defects', methods=['GET'])
def fix_defects():
    pass


def _distance_filter(dealer_zip, customer_zip, max_distance=10):
    zcdb = ZipCodeDatabase()
    dealer_lat_long = (zcdb[dealer_zip].latitude, zcdb[dealer_zip].longitude)
    customer_lat_long = (zcdb[customer_zip].latitude, zcdb[customer_zip].longitude)
    distance = vincenty(dealer_lat_long, customer_lat_long)
    print distance
    return distance < max_distance