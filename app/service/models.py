from app import db
import sqlalchemy as sa
from flask_security import UserMixin

class Dealer(db.Model, UserMixin):
    __tablename__ = 'dealer'
    id = sa.Column(sa.Integer, primary_key=True)
    email = sa.Column(sa.String(250), unique=True)
    name = sa.Column(sa.String(250), unique=True)
    password = sa.Column(sa.String(255))

    address = sa.Column(sa.String(250))
