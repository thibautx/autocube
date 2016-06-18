from app.app import db


class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(80))
    model = db.Column(db.String(80))
    year = db.Column(db.Integer)
    list_price = db.Column(db.Float)
    image_url = db.Column(db.String(1000))

    def __init__(self, **kwargs):
        super(Listing, self).__init__(**kwargs)

