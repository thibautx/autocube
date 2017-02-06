from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user
from app import db
from app.service.models import Dealer
from app.service.timekit import on_new_dealer

public_module = Blueprint('_public', __name__)


@public_module.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('_garage.garage_home'))
    else:
        return render_template('public/landing.html')


@public_module.route('/register-dealer', methods=['GET', 'POST'])
def register_dealer():
    """
    Registration for a dealer.

    """
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        zip = request.form['zip']

        dealer = Dealer(name=name, email=email, password=password, zip=zip)
        db.session.add(dealer)
        db.session.commit()

        timekit = on_new_dealer(dealer)

        # register the dealer's timekit
        return render_template("public/dealer_registered.html", timekit=timekit, email=dealer.email)

    else:
        return render_template('public/register_dealer/register_dealer.html')