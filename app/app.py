from flask import Flask, render_template
from flask.ext.admin import Admin
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)
admin = Admin(app, 'Admin', template_mode='bootstrap3')


@app.errorhandler(404)
def not_found(error):
    return '404'


@app.route('/')
def landing_page():
    return render_template('index.html')