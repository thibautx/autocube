import sqlalchemy as sa
from app import db
from sqlalchemy import orm
from datetime import datetime
from flask_security import UserMixin, RoleMixin
from app.profile.auth.models import SocialConnection

roles_users = db.Table('roles_users',
                       sa.Column('user_id', sa.Integer(), sa.ForeignKey('user.id')),
                       sa.Column('role_id', sa.Integer(), sa.ForeignKey('role.id')))

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(80))
    model = db.Column(db.String(80))
    year = db.Column(db.Integer)
    license_plate = db.Column(db.String, unique=True, nullable=True)
    vin = db.Column(db.String, unique=True, nullable=True)

    owner = orm.relationship('User', back_populates='cars')

    def __init__(self, **kwargs):
        super(Car, self).__init__(**kwargs)


class User(db.Model, UserMixin):
    id = sa.Column(sa.Integer, primary_key=True)
    login = sa.Column(sa.String(250), unique=True)
    email = sa.Column(sa.String(250), unique=True)
    password = sa.Column(sa.String(255))
    active = sa.Column(sa.Boolean)
    confirmed_at = sa.Column(sa.DateTime)
    created = sa.Column(sa.DateTime, default=datetime.now)
    is_staff = sa.Column(sa.Boolean)
    first_name = sa.Column(sa.String(120))
    last_name = sa.Column(sa.String(120))
    roles = orm.relationship('Role', secondary=roles_users, backref=orm.backref('users', lazy='dynamic'))
    cars = orm.relationship('Car', back_populates='owner')

    @property
    def cn(self):
        if not self.first_name or not self.last_name:
            return self.email
        return u"{} {}".format(self.first_name, self.last_name)

    @classmethod
    def by_email(cls, email):
        return cls.query().filter(cls.email == email).get()

    @property
    def gravatar(self):
        email = self.email.strip()
        if isinstance(email, unicode):
            email = email.encode("utf-8")
        import hashlib
        encoded = hashlib.md5(email).hexdigest()
        return "https://secure.gravatar.com/avatar/%s.png" % encoded

    def social_connections(self):
        return SocialConnection.query.filter(SocialConnection.user_id == self.id).all()


class Role(db.Model, RoleMixin):
    id = sa.Column(sa.Integer(), primary_key=True)
    name = sa.Column(sa.String(80), unique=True)
    description = sa.Column(sa.String(255))
