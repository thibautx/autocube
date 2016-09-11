from flask import Flask
from flask_admin import Admin
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DATABASE_URI'] = 'sqlite:///app.db'

# Configurations
app.config.from_object('config')

db = SQLAlchemy(app)

manager = Manager(app)
manager.add_command('db', MigrateCommand)
migrate = Migrate(app, db)

# Admin
from flask_admin.contrib.sqla import ModelView
from listing.models import Listing
from app.profile.models import User, Car
admin = Admin(app, 'Admin', template_mode='bootstrap3')
# admin.add_view(ModelView(Listing, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Car, db.session))

# Auth
from app.auth.models import init_app
init_app(app)

@app.errorhandler(404)
def not_found(error):
    return '404'


# Register blueprints
from app.index.controllers import index_module as mod_index
from app.news.controllers import news_module as mod_news
from app.auth.controllers import profile_module as mod_profile
# from app.listing.controllers import listing_module as mod_listing
from app.inventory.controllers import inventory_module as mod_inventory
from app.recalls.controllers import recalls_module as mod_recalls
app.register_blueprint(mod_index)
app.register_blueprint(mod_news)
app.register_blueprint(mod_profile)
# app.register_blueprint(mod_listing)
app.register_blueprint(mod_inventory)
app.register_blueprint(mod_recalls)

db.create_all()