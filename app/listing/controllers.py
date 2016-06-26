from app import db
from models import Listing
from flask import Blueprint, render_template

listing_module = Blueprint('_listing', __name__, url_prefix='/inventory/listing')

@listing_module.route('/<listing_id>')
def listing(listing_id):
    listing = db.session.query(Listing).filter(Listing.id == listing_id).all()[0].__dict__
    del(listing['_sa_instance_state'])
    return render_template('listing/index.html',
                           listing=listing)


@listing_module.route('/api/listing', methods=['GET'])
def listing_api():
    return 'foo'

@listing_module.route('/<listing_id>/deposit')
def deposit(listing_id):
    return 'foo'