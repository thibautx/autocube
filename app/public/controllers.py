from app.service.models import Dealer
from flask_login import current_user
from flask import Blueprint, render_template, redirect, url_for, request
from forms import DealerRegistrationForm
from app import db

public_module = Blueprint('public', __name__)


@public_module.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('_garage.garage_home'))
    else:
        return render_template('public/landing.html')


@public_module.route('/register-dealer', methods=['GET', 'POST'])
def register_dealer():
    form = DealerRegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        # name = request.form['name']
        # email = request.form['email']
        # password = request.form['password']
        name = form.name.data
        email = form.email.data
        password = form.password.data
        dealer = Dealer(name, email, password)
        db.session.add(dealer)
        db.session.commit()
        return 'dealer register success'

    else:
        return render_template('public/register_dealer/register_dealer.html',
                               form=form)