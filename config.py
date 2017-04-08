import os

DEBUG = True
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


SQLALCHEMY_DATABASE_URI = "postgresql://postgres:asdffdsa@localhost:5432/autocube"
# SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_TRACK_MODIFICATIONS = False
DATABASE_CONNECT_OPTIONS = {}
THREADS_PER_PAGE = 2
CSRF_ENABLED = True
CSRF_SESSION_KEY = "8a7474974efcf76896aa84eea9cbe016bbc08828"
SECRET_KEY = '47e585de7f22984d5ee291c2f31412384bfc32d0'
FLASH_MESSAGES = True
LOGIN_DISABLED = False
SECURITY_PASSWORD_SALT = "abc"
SECURITY_PASSWORD_HASH = "bcrypt"  # requires py-bcrypt
SECURITY_EMAIL_SENDER = "support@autocube.com"
SECURITY_CONFIRMABLE = True
SECURITY_REGISTERABLE = True
SECURITY_RECOVERABLE = True
SECURITY_CHANGEABLE = True
SECURITY_CONFIRM_SALT = "570be5f24e690ce5af208244f3e539a93b6e4f05"
SECURITY_REMEMBER_SALT = "de154140385c591ea771dcb3b33f374383e6ea47"
SECURITY_DEFAULT_REMEMBER_ME = True
BABEL_DEFAULT_LOCALE = "en"
BABEL_DEFAULT_TIMEZONE = "UTC"

# Flask-Mail
# http://pythonhosted.org/Flask-Mail/
SERVER_EMAIL = 'Autocube <mail@autocube.com>'

# Flask-SocialBlueprint
# https://github.com/wooyek/flask-social-blueprint
SOCIAL_BLUEPRINT = {
    # https://developers.facebook.com/apps/
    "flask_social_blueprint.providers.Facebook": {
        # App ID
        'consumer_key': '1736167959983448',
        # App Secret
        'consumer_secret': '3f28ce9bc466f2b295876b0d857f9bd2'
    },
     "flask_social_blueprint.providers.Google": {
        # Client ID
        'consumer_key': '580132776922-2ffpv4idfmqogf4tdnfr5sdpf60493m3.apps.googleusercontent.com',
        # Client secret
        'consumer_secret': 'AtOFNbtgBTLul1Di-t0hz0F6'
    },
}
