from flask import Blueprint, render_template

landing_module = Blueprint('landing', __name__)

@landing_module.route('/')
def home():
    return render_template('index.html')

@landing_module.route('/play')
def play():
    return render_template('play.html')