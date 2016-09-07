from flask import Flask, render_template
from flask_admin import Admin
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config['DATABASE_URI'] = 'sqlite:///app.db'

# Configurations
app.config.from_object('config')

db = SQLAlchemy(app)
db.create_all()


manager = Manager(app)
manager.add_command('db', MigrateCommand)
migrate = Migrate(app, db)


# Admin
from flask_admin.contrib.sqla import ModelView
from listing.models import Listing
admin = Admin(app, 'Admin', template_mode='bootstrap3')
admin.add_view(ModelView(Listing, db.session))

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return '404'


# Register blueprints
from app.index.controllers import index_module as mod_index
from app.listing.controllers import listing_module as mod_listing
from app.inventory.controllers import inventory_module as mod_inventory
from app.recalls.controllers import recalls_module as mod_recalls
app.register_blueprint(mod_index)
app.register_blueprint(mod_listing)
app.register_blueprint(mod_inventory)
app.register_blueprint(mod_recalls)


# @app.route('/')
# def landing_page():
#     return render_template('index.html')