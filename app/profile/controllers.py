from app import db
from flask import Blueprint, render_template

profile_module = Blueprint('_profile', __name__, url_prefix='/profile')

@profile_module.route('/')
def profile():
    pass