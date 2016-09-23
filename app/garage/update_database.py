import edmunds
from app import db
from app.garage.models import Car, Recall
from datetime import datetime
from sqlalchemy import func

def on_new_car_update_recalls(make, model, year):
    """
    :return:
    """

    # make/model/year for this car already exists in db
    if Car.query.filter(func.lower(Car.make) == func.lower(make) and
                        func.lower(Car.model) == func.lower(model) and
                        func.lower(Car.year) == func.lower(year)).count():
        return

    else:
        update_recalls()


def update_car_recalls(make, model, year):
    """
    Update recalls for a specific car
    :return:
    """
    pass


def update_recalls():
    """
    Update recalls for all cars in database.

    :return:
    """

    distinct_cars = Car.query.distinct(Car.model, Car.make, Car.year).all()
    for car in distinct_cars:
        print car.make, car.model, car.year

        recalls = edmunds.get_recalls(car.make, car.model, car.year)
        for recall in recalls:
            recall_id = recall['id']

            # recall already in database
            if Recall.query.filter(Recall.id == recall_id).count():
                print 'already in db'
                pass

            # add recall to database
            else:
                manufactured_from, manufactured_to = _manufactured_to_and_from(recall)
                db_recall = Recall(id=recall_id,
                                   nhtsa_number=recall['recallNumber'],
                                   consequence=recall['defectConsequence'],
                                   components=recall['componentDescription'],
                                   manufactured_from=manufactured_from,
                                   manufactured_to=manufactured_to)

                car.recalls.append(db_recall)  # add recall to the car
                db.session.add(db_recall)      # add recall to the db
                db.session.commit()


def _manufactured_to_and_from(recall):
    try:
        manufactured_from = datetime.strptime(recall['manufacturedFrom'], "%Y-%m-%d").date()
    except KeyError:
        manufactured_from = None
    try:
        manufactured_to = datetime.strptime(recall['manufacturedTo'], "%Y-%m-%d").date()
    except KeyError:
        manufactured_to = None

    return manufactured_from, manufactured_to

if __name__ == "__main__":
    make = 'audi'
    model = 'a4'
    year = 2012
    # print on_new_car_update_recalls(make, model, year)
    update_recalls()
    # manufactured_to = '2012-10-29'
    # print datetime.strptime(manufactured_to, "%Y-%m-%d").date()