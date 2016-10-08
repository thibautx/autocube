import json
from app.garage import edmunds
from flask import Blueprint, render_template, request, jsonify, redirect, url_for

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

@service_module.route('/fix-defects', methods=['GET'])
def fix_defects():
    pass