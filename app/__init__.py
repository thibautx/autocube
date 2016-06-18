from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

# Configurations
app.config.from_object('config')

db = SQLAlchemy(app)

# Admin
from flask_admin.contrib.sqla import ModelView
from inventory.models import Listing
admin = Admin(app, 'Admin', template_mode='bootstrap3')
admin.add_view(ModelView(Listing, db.session))

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return '404'


# Register blueprints
from app.inventory.controllers import inventory_module as mod_inventory
app.register_blueprint(mod_inventory)

db.create_all()

@app.route('/')
def landing_page():
    return render_template('index.html')