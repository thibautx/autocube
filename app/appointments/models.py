# from app import db
# from sqlalchemy import orm
# import sqlalchemy as sa
#
# class TimeKitUser(db.Model):
#     """
#
#     """
#     __tablename__ = 'timekit'
#
#     id = sa.Column(sa.Integer, primary_key=True)
#
#     password = db.Column(db.String)
#
#     app_id = db.Column(sa.String)
#     email = db.Column(sa.String)
#     timezone = db.Column(sa.String)
#     calendar_id = db.Column(sa.String)  # default calendar
#
#     user_id = db.Column(sa.Integer, sa.ForeignKey('user.id'))
#
#     def __init__(self, **kwargs):
#         super(TimeKitUser, self).__init__(**kwargs)