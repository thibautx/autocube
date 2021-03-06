import sqlalchemy as sa
from sqlalchemy import orm, Enum
from app.garage.edmunds import try_get_image

from app import db

recalls_cars = db.Table('recalls_cars',
                        sa.Column('car_id', sa.Integer(), sa.ForeignKey('car.id')),
                        sa.Column('recall_id', sa.Integer(), sa.ForeignKey('recall.id')))

recalls_service = db.Table('recalls_service',
                           sa.Column('car_id', sa.Integer(), sa.ForeignKey('car.id')),
                           sa.Column('service_bulletin_id', sa.Integer(), sa.ForeignKey('service_bulletin.id')))


class Car(db.Model):
    __tablename__ = 'car'
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(80))
    make_no_space = db.Column(db.String(80))
    model = db.Column(db.String(80))
    model_no_space = db.Column(db.String(80))
    year = db.Column(db.Integer)
    vin = db.Column(db.String, unique=True, nullable=True)
    current_mileage = db.Column(db.Integer, nullable=True)
    transmission_type = db.Column(Enum('automatic', 'manual', name='transmission_types'))
    image_url = db.Column(db.String)

    user_id = db.Column(sa.Integer, sa.ForeignKey('user.id'))
    user = orm.relationship('User', foreign_keys=user_id, backref=orm.backref('user', order_by=id))

    recalls = orm.relationship('Recall', secondary=recalls_cars,
                               backref=orm.backref('recalls', lazy='dynamic'))
    service_bulletins = orm.relationship('ServiceBulletin', secondary=recalls_service,
                                         backref=orm.backref('recalls', lazy='dynamic'))

    service_date = db.Column(db.DateTime)

    def __init__(self, **kwargs):
        super(Car, self).__init__(**kwargs)
        self.make_no_space = self.make.replace(' ', '')
        self.model_no_space = self.model.replace(' ', '')
        self.image_url = try_get_image(self.make_no_space, self.model_no_space, self.year)


class ServiceBulletin(db.Model):
    __tablename__ = 'service_bulletin'
    id = db.Column(db.Integer, primary_key=True)
    service_bulletin_id = db.Column(db.String)

    date = db.Column(db.Date)                       # bulletinDate
    component_number = db.Column(db.Integer)        # componentNumber
    component_description = db.Column(db.String)    # componentDescription
    bulletin_number = db.Column(db.String)          # bulletinNumber
    nhtsa_number = db.Column(db.String)             # nhtsaItemNumber
    summary = db.Column(db.String)                  # summaryText

    dealer_id = db.Column(db.Integer)               # dealer that's fixing this
    active = db.Column(db.Boolean)
    date_fixed = db.Column(db.Date, nullable=True)



    def __init__(self, **kwargs):
        super(ServiceBulletin, self).__init__(**kwargs)

    def set_dealer(self, dealer_id):
        self.dealer_id = dealer_id
        db.session.commit()


class Recall(db.Model):
    __tablename__ = 'recall'
    id = db.Column(db.Integer, primary_key=True)
    recall_id = db.Column(db.String)

    nhtsa_number = db.Column(db.String)
    consequence = db.Column(db.String)
    components = db.Column(db.String)

    manufactured_from = db.Column(db.Date)
    manufactured_to = db.Column(db.Date)

    dealer_id = db.Column(db.Integer)
    fixed = db.Column(db.Boolean)
    date_fixed = db.Column(db.String, nullable=True)

    def __init__(self, **kwargs):
        super(Recall, self).__init__(**kwargs)

    def set_dealer(self, dealer_id):
        self.dealer_id = dealer_id
        db.session.commit()