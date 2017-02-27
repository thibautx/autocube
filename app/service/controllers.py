from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from flask_user import roles_required
from geopy.distance import vincenty
from pyzipcode import ZipCodeDatabase

from app.garage import edmunds
from app.garage.models import Car
from app.service.models import Dealer

service_module = Blueprint('_service', __name__, url_prefix='/service')


@service_module.route('/dealer-home')
@login_required
def dealer_home():
    if current_user.is_dealer is False:
        return redirect(url_for('_garage.garage_home'))


    return render_template('service/dealer_home.html')

@service_module.route('/')
def home():
    """
    Default page for dealers.

    :return:
    """
    makes = edmunds.get_makes()
    return render_template("service/index.html",
                           makes=makes)


@service_module.route('/dealers')
def list_dealers():
    if request.method == 'GET':
        make = request.args['make']
        zip = request.args['zip']
        dealers = edmunds.get_dealers(zip, make)
        all_autocube_dealers = Dealer.query.all()
        autocube_dealers = [dealer for dealer in all_autocube_dealers if _distance_filter(dealer.zip, zip) == True]
        return render_template('service/list_dealers.html',
                               autocube_dealers=autocube_dealers,
                               dealers=dealers)

# @service_module.route('/dealers', methods=['GET'])
# def list_dealers():
#     if request.method == 'GET':
#         makes = json.dumps(edmunds.get_makes())
#         make = request.args['make']
#         zip = request.args['zip']
#         dealers = []
#         return render_template("service/index.html",
#                                makes=makes,
#                                dealers=dealers)


@service_module.route('/schedule/<dealer_id>/<car_id>')
def schedule_with_dealer(dealer_id, car_id):
    car = Car.query.filter(Car.id == car_id)[0]
    dealer = Dealer.query.filter(Dealer.id == dealer_id)[0]
    return render_template('service/dealer_schedule.html',
                           dealer=dealer,
                           car=car)


@service_module.route('/car/<car_id>/service/campaign_number=', methods=['POST'])
def service_car(car_id):
    car = Car.query.get(car_id)
    target_zip = request.form['zip']

    try:
        max_distance = request.form['distance']
    except KeyError:
        max_distance = 10

    dealers = edmunds.get_dealers(target_zip, car.make)
    all_autocube_dealers = Dealer.query.all()
    autocube_dealers = [dealer for dealer in all_autocube_dealers if _distance_filter(dealer.zip, target_zip, max_distance) == True]
    return render_template('service/list_dealers.html',
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

