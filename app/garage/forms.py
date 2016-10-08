from wtforms import Form, IntegerField, StringField, validators

class CarDetailsForm(Form):
    current_mileage = IntegerField('Current mileage')
    vin = StringField('VIN')
