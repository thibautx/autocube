from app import db
from models import Listing
from sqlalchemy import select
from flask import Blueprint, request, render_template, jsonify

"""
TODO:
    - sort current view by year, price, model, distance
    - filter by year, make, model, price
"""

inventory_module = Blueprint('inventory', __name__, url_prefix='/inventory')

def get_all_listings():
    all_listings = Listing.query.all()
    return all_listings


def get_all_makes():
    """
    Get all makes.

    :param model:
    :return:
    """
    return sorted([row.make for row in db.session.query(Listing.make.distinct().label('make')).all()])


def get_all_models(make):
    """
    Get all the possible models by the make (sorted alphabetically)

    :param make: (str)
    :return: (list of str)
    """
    return sorted([row.model for row in db.session.query(Listing.model).filter(Listing.make == make).distinct().all()])


@inventory_module.route('/api/makes', methods=['GET'])
def api_makes():
    return jsonify(makes=get_all_makes())


@inventory_module.route('/api/models', methods=['POST'])
def api_models():
    make = request.form['make']
    print get_all_models(make)
    return jsonify(models=get_all_models(make))


@inventory_module.route('/')
def list_inventory():
    all_listings = get_all_listings()
    return render_template('inventory/index.html',
                           listings=all_listings)


@inventory_module.route('/')
def list_inventory_sorted(sort='list_price'):
    pass
