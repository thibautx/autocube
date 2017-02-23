import sqlalchemy as sa
from flask_security import UserMixin
from sqlalchemy import orm
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from app import db, bcrypt
from geopy.distance import vincenty
import zipcode


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

    cars = sa.column(JSON)

    # user_id = db.Column(sa.Integer, sa.ForeignKey('user.id'))
    # user = orm.relationship('User', foreign_keys=user_id, backref=orm.backref('user', order_by=id))