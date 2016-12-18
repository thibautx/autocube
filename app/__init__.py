from flask import Flask
from flask_admin import Admin
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
# from flask_cache import Cache


app = Flask(__name__)
bcrypt = Bcrypt(app)
# cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# Configurations
app.config.from_object('config')

db = SQLAlchemy(app)


manager = Manager(app)
manager.add_command('db', MigrateCommand)
migrate = Migrate(app, db)

# Admin
from flask_admin.contrib.sqla import ModelView
from app.profile.models import User
from app.service.models import Dealer
from app.garage.models import Car, Recall, ServiceBulletin
from app.auth.models import SocialConnection

admin = Admin(app, 'Admin', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Dealer, db.session))
admin.add_view(ModelView(Car, db.session))
admin.add_view(ModelView(SocialConnection, db.session))
admin.add_view(ModelView(Recall, db.session))
admin.add_view(ModelView(ServiceBulletin, db.session))

# Auth
from app.auth.models import init_app
init_app(app)

# Register blueprints
from app.public.controllers import public_module as mod_public
from app.news.controllers import news_module as mod_news
from app.profile.controllers import profile_module as mod_profile
from app.garage.controllers import garage_module as mod_recalls
# from app.appointments.controllers import appointments_module as mod_appointments
from app.service.controllers import service_module as mod_service
app.register_blueprint(mod_public)
app.register_blueprint(mod_news)
app.register_blueprint(mod_profile)
app.register_blueprint(mod_recalls)
# app.register_blueprint(mod_appointments)
app.register_blueprint(mod_service)


db.create_all()