import nhtsa
from flask import Blueprint, render_template, request

recalls_module = Blueprint('_recalls', __name__, url_prefix='/recalls')

@recalls_module.route('/')
def recalls():
    return render_template('recalls/index.html')

@recalls_module.route('/filter', methods=['GET', 'POST'])
def filter():
    if request.method == 'GET':

        year = request.args.get('year')
        make = request.args.get('make')
        model = request.args.get('model')
        recalls = nhtsa.get_recalls(year, make, model)
        return render_template('recalls/index.html', recalls=recalls)