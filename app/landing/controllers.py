from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

landing_module = Blueprint('landing', __name__)

# from flask_wtf import Form, TextField, PasswordField, validators
# from myapplication.models import User

#
# class LoginForm(Form):
#     username = TextField('Username', [validators.Required()])
#     password = PasswordField('Password', [validators.Required()])
#
#     def __init__(self, *args, **kwargs):
#         Form.__init__(self, *args, **kwargs)
#         self.user = None
#
#     def validate(self):
#         rv = Form.validate(self)
#         if not rv:
#             return False
#
#         user = User.query.filter_by(
#             username=self.username.data).first()
#         if user is None:
#             self.username.errors.append('Unknown username')
#             return False
#
#         if not user.check_password(self.password.data):
#             self.password.errors.append('Invalid password')
#             return False
#
#         self.user = user
#         return True

@landing_module.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('_garage.garage_home'))
    else:
        return render_template('index.html')

@landing_module.route('/register-dealer')
def register_dealer():
    return render_template('register_dealer.html')