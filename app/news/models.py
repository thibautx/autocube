import sqlalchemy as sa

from app import db

class NewsItem(db.Model):
    __tablename__ = 'news_item'

    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String)
