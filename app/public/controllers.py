from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user
from app import db
from app.profile.models import User
from app.service.models import Dealer
from app.service.timekit import on_new_dealer
from app.garage.edmunds import get_makes
import json

public_module = Blueprint('public', __name__)


@public_module.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('_garage.garage_home'))
    else:
        return render_template('public/landing.html')


@public_module.route('/login-user', methods=['GET','POST'])
def login():

    if request.method == 'POST':
        print "attempt login user"
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).all()
        if len(user) == 0:
            flash("Invalid password, try again.")
            return redirect(url_for('.login'))

        else:
            user = user[0]

        if user.is_correct_password(password):
            print 'correct password'
            login_user(user, force=True)
            return redirect(url_for('_garage.garage_home'))

    else:
        return render_template('security/login_user.html')


@public_module.route('/register-user', methods=['GET', 'POST'])
def register_by_email():
    if request.method == 'POST':

        if len(User.query.filter_by(email=request.form['email']).all()) > 0:
            flash('E-mail {} already registered, please log in.'.format(request.form['email']))
            return redirect(url_for('security.login'))

        user = User(email=request.form['email'],
                    first_name=request.form['first_name'],
                    last_name=request.form['last_name'])
        user._set_password = request.form['password']
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('security.login'))
    # else:
    #     return render_template('security/register_user.html')


@public_module.route('/register-dealer', methods=['GET', 'POST'])
def register_dealer():
    """
    Registration for a dealer.

    """
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        _zip = request.form['zip']
        makes_serviced = json.dumps({
            make : 1 for make in request.form.getlist('makes')
        })
        website = request.form['website']
        phone = request.form['phone']

        dealer = Dealer(name=name,
                        email=email,
                        zip=_zip,
                        makes_serviced=makes_serviced,
                        website=website,
                        phone=phone)
        db.session.add(dealer)
        db.session.commit()

        user = User(email=email,
                    dealer=dealer,
                    is_dealer=True,
                    first_name=name)
        user._set_password = password
        db.session.add(user)
        db.session.commit()

        timekit = on_new_dealer(dealer)

        # register the dealer's timekit
        return render_template("public/dealer_registered.html", timekit=timekit, email=dealer.email)

    else:
        makes = get_makes()
        return render_template('public/register_dealer/register_dealer.html', makes=makes)


@public_module.route('/login-dealer',methods=['GET','POST'])
def login_dealer():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first_or_404()
        if user.is_correct_password(password):
            login_user(user, force=True)
            return redirect(url_for('_service.dealer_home'))

    else:
        return render_template('security/login_dealer.html')