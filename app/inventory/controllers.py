# from flask import Blueprint, request, render_template, jsonify
#
# from app.inventory.util import get_all_makes, get_all_models, get_all_listings, get_listings_by_make, \
#     get_listings_by_make_model
#
# """
# TODO:
#     - sort current view by year, price, model, distance
#     - filter by year, make, model, price
# """
#
# inventory_module = Blueprint('inventory', __name__, url_prefix='/inventory')
#
#
# @inventory_module.route('/api/makes', methods=['GET'])
# def api_makes():
#     return jsonify(makes=get_all_makes())
#
#
# @inventory_module.route('/api/models', methods=['POST'])
# def api_models():
#     make = request.form['make']
#     return jsonify(models=get_all_models(make))
#
#
# @inventory_module.route('/')
# def inventory():
#     listings = get_all_listings()
#     makes = get_all_makes()
#     return render_template('inventory/landing.html',
#                            listings=listings, makes=makes)
#
# @inventory_module.route('/filter', methods=['GET', 'POST'])
# def filter():
#     if request.method == 'GET':
#
#         makes = get_all_makes()
#
#         # filter by make
#         make = request.args.get('make')
#         models = get_all_models(make)
#         listings = get_listings_by_make(make)
#
#         # filter by make and model
#         model = request.args.get('model')
#         if model is not None:
#             listings = get_listings_by_make_model(make, model)
#
#         return render_template('inventory/landing.html',
#                                listings=listings, makes=makes, models=models)
#
#
# @inventory_module.route('/')
# def list_inventory_sorted(sort='list_price'):
#     pass
