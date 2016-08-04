from app import db
from flask import Blueprint, request, render_template, jsonify

index_module = Blueprint('index', __name__, url_prefix='/')

# SOCIAL_BLUEPRINT = {
#     # https://developers.facebook.com/apps/
#     "flask_social_blueprint.providers.Facebook": {
#         # App ID
#         'consumer_key': '',
#         # App Secret
        # 'consumer_secret': '',
#     },
# }
#

@index_module.route('/login/facebook')
def facebook_login():
    pass

@index_module.route('/')
def index():
    return render_template('index.html')