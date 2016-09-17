import sqlalchemy as sa
from sqlalchemy import orm, Enum, Table
from app import db


class Car(db.Model):
    __tablename__ = 'car'
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(80))
    model = db.Column(db.String(80))
    year = db.Column(db.Integer)
    vin = db.Column(db.String, unique=True, nullable=True)
    current_mileage = db.Column(db.Integer, nullable=True)
    transmission_type = db.Column(Enum('automatic', 'manual', name='transmission_types'))

    user_id = db.Column(sa.Integer, sa.ForeignKey('user.id'))
    user = orm.relationship('User', foreign_keys=user_id, backref=orm.backref('user', order_by=id))

    def __init__(self, **kwargs):
        super(Car, self).__init__(**kwargs)