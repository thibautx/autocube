import logging
from datetime import datetime
import sqlalchemy as sa
from flask import current_app
from flask_babel import gettext as _
from flask_security import Security, SQLAlchemyUserDatastore
from sqlalchemy import orm
from app import db
from app.profile.models import User, Role


class SocialConnection(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('user.id'))
    user = orm.relationship('User', foreign_keys=user_id, backref=orm.backref('connections', order_by=id))
    provider = sa.Column(sa.String(255))
    profile_id = sa.Column(sa.String(255))
    username = sa.Column(sa.String(255))
    email = sa.Column(sa.String(255))
    access_token = sa.Column(sa.String(255))
    secret = sa.Column(sa.String(255))
    first_name = sa.Column(sa.String(255))
    last_name = sa.Column(sa.String(255))
    cn = sa.Column(sa.String(255))
    profile_url = sa.Column(sa.String(512))
    image_url = sa.Column(sa.String(512))

    def get_user(self):
        return self.user

    @classmethod
    def by_profile(cls, profile):
        provider = profile.data["provider"]
        return cls.query.filter(cls.provider == provider, cls.profile_id == profile.id).first()

    @classmethod
    def from_profile(cls, user, profile):
        if not user or user.is_anonymous:
            email = profile.data.get("email")
            if not email:
                msg = "Cannot create new user, authentication provider did not not provide email"
                logging.warning(msg)
                raise Exception(_(msg))
            conflict = User.query.filter(User.email == email).first()
            if conflict:
                msg = "Cannot create new user, email {} is already used. Login and then connect external profile."
                msg = _(msg).format(email)
                logging.warning(msg)
                raise Exception(msg)

            now = datetime.now()
            user = User()
            print type(profile)
            print profile.__dict__
            user.email = email
            user.first_name = profile.data.get('first_name')
            user.last_name = profile.data.get('last_name')
            user.confirmed_at = now
            user.active = True
            db.session.add(user)
            db.session.flush()

        assert user.id, "User does not have an id"
        connection = cls(user_id=user.id, **profile.data)
        db.session.add(connection)
        db.session.commit()
        return connection


def load_user(user_id):
    return User.query.get(user_id)


def send_mail(msg):
    logging.debug("msg: %s" % msg)
    mail = current_app.extensions.get('mail')
    mail.send(msg)


def init_app(app):
    from flask_login import LoginManager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.user_loader(load_user)
    login_manager.login_view = "/login"

    # Setup Flask-Security
    from flask_security.forms import ChangePasswordForm
    security = Security()
    security = security.init_app(app, SQLAlchemyUserDatastore(db, User, Role),
                                 change_password_form=ChangePasswordForm)
    security.send_mail_task(send_mail)


    from flask_social_blueprint.core import SocialBlueprint
    SocialBlueprint.init_bp(app, SocialConnection, url_prefix="/auth")
