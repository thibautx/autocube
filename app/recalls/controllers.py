import json
import nhtsa
import edmunds
from app import db
from app.profile.models import Car
from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user

recalls_module = Blueprint('_recalls', __name__, url_prefix='/recalls')

@recalls_module.route('/')
@login_required
def recalls():
    makes = edmunds.get_makes()
    cars = Car.query.filter(Car.user_id == current_user.id).all()
    return render_template('recalls/garage.html', cars=cars, makes=json.dumps(makes))

@recalls_module.route('/add-car', methods=['POST'])
@login_required
def add_car():
    if request.method == 'POST':
        make = request.form['make']
        model = request.form['model']
        year = request.form['year']
        car = Car(make=make, model=model, year=year, user_id=current_user.id)
        db.session.add(car)
        db.session.commit()
        return redirect(url_for('.recalls'))

@recalls_module.route('/remove-car', methods=['POST'])
@login_required
def remove_car():
    pass

@recalls_module.route('/models', methods=['GET'])
def models():
    if request.method == 'GET':
        make = request.args.get('make')
        models = edmunds.get_models(make)
        return json.dumps(models)

@recalls_module.route('/model-years', methods=['GET'])
def model_years():
    if request.method == 'GET':
        make = request.args.get('make')
        model = request.args.get('model')
        model_years = edmunds.get_model_years(make, model)
        return json.dumps(model_years)


# @recalls_module.route('/filter', methods=['GET', 'POST'])
# def filter():
#     if request.method == 'GET':
#         year = request.args.get('year')
#         make = request.args.get('make')
#         model = request.args.get('model')
#         recalls = nhtsa.get_recalls(year, make, model)
#         dealers = edmunds.get_dealers(60601, make)
#         return render_template('recalls/index.html', recalls=recalls, dealers=dealers)
