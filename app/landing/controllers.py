from flask import Blueprint, render_template

landing_module = Blueprint('landing', __name__)

@landing_module.route('/')
def home():
    return render_template('index.html')

