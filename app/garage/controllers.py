import json
import nhtsa
import edmunds
from app import db
from app.garage.models import Car
from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user

garage_module = Blueprint('_recalls', __name__, url_prefix='/garage')

@garage_module.route('/')
@login_required
def garage():
    makes = edmunds.get_makes()
    cars = Car.query.filter(Car.user_id == current_user.id).all()
    return render_template('garage/garage.html', cars=cars, makes=json.dumps(makes))

@garage_module.route('/car/<id>')
def car_details(id):
    car = Car.query.get(id)
    return render_template('garage/car.html', car=car)

@garage_module.route('/car', methods=['POST'])
@login_required
def add_car():
    if request.method == 'POST':
        make = request.form['make']
        model = request.form['model']
        year = request.form['year']
        car = Car(make=make, model=model, year=year, user_id=current_user.id)
        db.session.add(car)
        db.session.commit()
        return redirect(url_for('.garage'))


@garage_module.route('/car/delete/<int:id>', methods=['POST'])
def remove_car(id):
    if request.method == 'POST':
        db.session.delete(Car.query.get(id))
        db.session.commit()
        return redirect(url_for('.garage'))


@garage_module.route('/car/update/<int:id>', methods=['POST'])
def update_car(id):
    if request.method == 'POST':
        car = Car.query.get(id)
        args = request.form.to_dict()
        for arg, value in args.items():
            setattr(car, arg, value)
        db.session.commit()
        return redirect(url_for('.car_details', id=id))


@garage_module.route('/models', methods=['GET'])
def models():
    if request.method == 'GET':
        make = request.args.get('make')
        models = edmunds.get_models(make)
        return json.dumps(models)


@garage_module.route('/model-years', methods=['GET'])
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
#         garage = nhtsa.get_recalls(year, make, model)
#         dealers = edmunds.get_dealers(60601, make)
#         return render_template('garage/index.html', garage=garage, dealers=dealers)
