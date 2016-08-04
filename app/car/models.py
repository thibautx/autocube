from app import db


class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(80))
    model = db.Column(db.String(80))
    year = db.Column(db.Integer)
    mileage = db.Column(db.Integer, nullable=True)

    license_plate = db.Column(db.String, unique=True, nullable=True)
    vin = db.Column(db.String, unique=True, nullable=True)

    list_price = db.Column(db.Float)
    image_url = db.Column(db.String(1000))

    def __init__(self, **kwargs):
        super(Car, self).__init__(**kwargs)

