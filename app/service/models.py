import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import orm
from app import db


cars_dealers = db.Table('cars_dealers',
                      sa.Column('dealer_id', sa.Integer(), sa.ForeignKey('dealer.id')),
                      sa.Column('car_id', sa.Integer(), sa.ForeignKey('car.id')))


class Dealer(db.Model):
    __tablename__ = 'dealer'
    id = sa.Column(sa.Integer, primary_key=True)

    email = sa.Column(sa.String(250), unique=True)
    name = sa.Column(sa.String(250), unique=True)
    _password = sa.Column(sa.String(255))

    website = sa.Column(sa.String(100))
    phone = sa.Column(sa.String(15))
    address = sa.Column(sa.String(250))
    zip = sa.Column(sa.Integer)

    makes_serviced = sa.Column(JSON)
    timekit = sa.Column(JSON)


    cars_serviced = orm.relationship('Car', secondary=cars_dealers, backref=orm.backref('dealers', lazy='dynamic'))
