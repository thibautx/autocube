from app.app import app, db, admin

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

# Configurations
app.config.from_object('config')

# Admin
from flask_admin.contrib.sqla import ModelView
from inventory.models import Listing

admin.add_view(ModelView(Listing, db.session))

# Sample HTTP error handling


# Register blueprints
from app.inventory.controllers import inventory_module as mod_inventory
app.register_blueprint(mod_inventory)

db.create_all()

