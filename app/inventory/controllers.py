from app import db
from models import Listing
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for

inventory_module = Blueprint('inventory', __name__, url_prefix='/inventory')

@inventory_module.route('/')
def inventory():

    listings = Listing.query.all()
    print type(listings)

    return render_template('inventory/index.html',
                           listings=listings)

def list_all_cars(sortby='list_price'):
    pass