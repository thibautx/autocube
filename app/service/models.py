import sqlalchemy as sa
from flask_security import UserMixin
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from app import db, bcrypt
from geopy.distance import vincenty
import zipcode


class Dealer(db.Model, UserMixin):
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


    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def _set_password(self, plaintext):
        self._password = bcrypt.generate_password_hash(plaintext)

    def is_correct_password(self, plaintext):
        return bcrypt.check_password_hash(self._password, plaintext)


    # @hybrid_method
    # def distance(self, zip, max_distance=10):
    #     # zcdb = ZipCodeDatabase()
    #     # dealer_lat_long = (zcdb[self.zip].latitude, zcdb[self.zip].longitude)
    #     # customer_lat_long = (zcdb[zip].latitude, zcdb[zip].longitude)
    #     # distance = vincenty(dealer_lat_long, customer_lat_long)
    #     # return distance < max_distance
    #     return True