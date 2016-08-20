from flask import Blueprint, request, render_template, jsonify
from app.inventory.util import get_all_makes, get_all_models
from app.listing.models import Listing

"""
TODO:
    - sort current view by year, price, model, distance
    - filter by year, make, model, price
"""

inventory_module = Blueprint('inventory', __name__, url_prefix='/inventory')

def get_all_listings():
    all_listings = Listing.query.all()
    return all_listings


def get_listings_by_make(make):
    listings = Listing.query.filter(Listing.make == make).all()
    return listings

@inventory_module.route('/api/makes', methods=['GET'])
def api_makes():
    return jsonify(makes=get_all_makes())


@inventory_module.route('/api/models', methods=['POST'])
def api_models():
    make = request.form['make']
    return jsonify(models=get_all_models(make))


@inventory_module.route('/')
def inventory(make=None, model=None, year=None):

    if make is None and model is None and year is None:
        listings = get_all_listings()
    else:
        listings = get_listings_by_make(make)

    all_makes = get_all_makes()
    return render_template('inventory/index.html',
                           listings=listings, all_makes=all_makes, make=make)

@inventory_module.route('/filter', methods=['GET', 'POST'])
def filter():
    print request.method
    if request.method == 'GET':
        make = request.args.get('make')
        return inventory(make=make)


@inventory_module.route('/')
def list_inventory_sorted(sort='list_price'):
    pass
