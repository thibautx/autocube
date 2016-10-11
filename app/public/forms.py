from flask_wtf import Form
from wtforms import StringField, PasswordField, validators


class DealerRegistrationForm(Form):
    name = StringField('Name', [validators.Length(min=4, max=20)])
    email = StringField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Confirm Password')


