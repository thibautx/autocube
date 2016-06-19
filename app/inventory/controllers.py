from app import db
from models import Listing
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for

"""
TODO:
    - sort current view by year, price, model, distance
    - filter by year, make, model, price
"""

inventory_module = Blueprint('inventory', __name__, url_prefix='/inventory')

def get_all_listings():
    all_listings = Listing.query.all()
    makes = sorted([row.make for row in db.session.query(Listing.make.distinct().label('make')).all()])

    print 'makes', makes

    return all_listings

# TODO: test
def get_all_models():
    models = db.session.query(Listing.model).distinct().all()

# TODO: test
def get_all_makes(model):
    pass

@inventory_module.route('/')
def list_inventory():
    all_listings = get_all_listings()
    return render_template('inventory/index.html',
                           listings=all_listings)


@inventory_module.route('/')
def list_inventory_sorted(sort='list_price'):
    pass