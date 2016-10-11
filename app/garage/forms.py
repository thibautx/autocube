from wtforms import Form, IntegerField, StringField


class CarDetailsForm(Form):
    current_mileage = IntegerField('Current mileage')
    vin = StringField('VIN')
