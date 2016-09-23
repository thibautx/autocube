import sqlalchemy as sa
from sqlalchemy import orm, Enum, Table
from app import db

recalls_cars = db.Table('recalls_cars',
                        sa.Column('car_id', sa.Integer(), sa.ForeignKey('car.id')),
                        sa.Column('recall_id', sa.Integer(), sa.ForeignKey('recall.id')))

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

    recalls = orm.relationship('Recall', secondary=recalls_cars, backref=orm.backref('recalls', lazy='dynamic'))

    def __init__(self, **kwargs):
        super(Car, self).__init__(**kwargs)

class ServiceBulletin(db.Model):
    __tablename__ = 'service_bulletin'
    id = db.Column(db.Integer, primary_key=True)

class Recall(db.Model):
    __tablename__ = 'recall'
    id = db.Column(db.Integer, primary_key=True)

    nhtsa_number = db.Column(db.String)
    consequence = db.Column(db.String)
    components = db.Column(db.String)
    date = db.Column(db.Date)

    manufactured_from = db.Column(db.Date)
    manufactured_to = db.Column(db.Date)

    def __init__(self, id, nhtsa_number, consequence, components, manufactured_from, manufactured_to):
        self.id = id
        self.nhtsa_number = nhtsa_number
        self.consequence = consequence
        self.components = components
        self.manufactured_from = manufactured_from
        self.manufactured_to = manufactured_to