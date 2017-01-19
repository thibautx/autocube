import re
from datetime import datetime

from sqlalchemy import func

import edmunds
from app import db
from app.garage.models import Car, Recall, ServiceBulletin


# RECALLS
def on_new_car_update_recalls(make, model, year):
    """


    :param make:
    :param model:
    :param year:
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

    :param make:
    :param model:
    :param year:
    :return:
    """
    return make, model, year


def update_recalls():
    """
    Update recalls for all cars in database.

    :return:
    """

    distinct_cars = Car.query.distinct(Car.model, Car.make, Car.year).all()
    for car in distinct_cars:
        recalls = edmunds.get_recalls(car.make, car.model, car.year)
        for recall in recalls:
            recall_id = recall['id']

            # recall already in database
            if Recall.query.filter(Recall.id == recall_id).count():
                pass

            # add recall to database
            else:
                manufactured_from, manufactured_to = _manufactured_to_and_from(recall)
                consequence = re.sub('([a-zA-Z])',
                                     lambda x: x.groups()[0].upper(),
                                     recall['defectConsequence'].lower(), 1)
                components = ', '.join(recall['componentDescription'].split(':'))
                db_recall = Recall(id=recall_id,
                                   nhtsa_number=recall['recallNumber'],
                                   consequence=consequence,
                                   components=components,
                                   manufactured_from=manufactured_from,
                                   manufactured_to=manufactured_to)

                car.recalls.append(db_recall)  # add recall to the car
                db.session.add(db_recall)  # add recall to the db
                db.session.commit()


def update_all_recalls():
    distinct_cars = Car.query.distinct(Car.model, Car.make, Car.year).all()
    for car in distinct_cars:
        print car.make, car.model, car.year

        recalls = edmunds.get_recalls(car.make, car.model, car.year)
        for recall in recalls:
            recall_id = recall['id']

            # recall already in database
            if Recall.query.filter(Recall.id == recall_id).count():
                pass

            # add recall to database
            else:
                manufactured_from, manufactured_to = _manufactured_to_and_from(recall)
                consequence = re.sub('([a-zA-Z])',
                                     lambda x: x.groups()[0].upper(),
                                     recall['defectConsequence'].lower(), 1)
                components = ', '.join(recall['componentDescription'].split(':'))
                db_recall = Recall(id=recall_id,
                                   nhtsa_number=recall['recallNumber'],
                                   consequence=consequence,
                                   components=components,
                                   manufactured_from=manufactured_from,
                                   manufactured_to=manufactured_to)

                car.recalls.append(db_recall)  # add recall to the car
                db.session.add(db_recall)  # add recall to the db
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


# SERVICE BULLETINS
def on_new_car_update_service_bulletins(make, model, year):
    # TODO: implement
    pass


def update_car_service_bulletins(make, model, year):
    # TODO: implement
    pass


def update_service_bulletins():
    """
    Update service bulletins for all cars in database.

    :return:
    """
    distinct_cars = Car.query.distinct(Car.model, Car.make, Car.year).all()
    for car in distinct_cars:
        print car.make, car.model, car.year

        service_bulletins = edmunds.get_service_bulletins(car.make, car.model, car.year)
        for service_bulletin in service_bulletins:
            service_bulletin_id = service_bulletin['id']

            # service bulletin  already in database
            if ServiceBulletin.query.filter(ServiceBulletin.id == service_bulletin_id).count():
                print 'already in db'
                pass

            # add service bulletin to database
            else:
                bulletin_date = datetime.strptime(service_bulletin['bulletinDate'], "%Y-%m-%d").date()
                try:
                    summary = re.sub('([a-zA-Z])',
                                     lambda x: x.groups()[0].upper(),
                                     service_bulletin['summaryText'].lower(), 1)
                except KeyError:
                    continue  # skip if no summary

                db_service_bulletin = ServiceBulletin(id=service_bulletin_id,
                                                      date=bulletin_date,
                                                      component_number=service_bulletin['componentNumber'],
                                                      component_description=service_bulletin['componentDescription'],
                                                      bulletin_number=service_bulletin['bulletinNumber'],
                                                      nhtsa_number=service_bulletin['nhtsaItemNumber'],
                                                      summary=summary,
                                                      )

                car.service_bulletins.append(db_service_bulletin)  # add recall to the car
                db.session.add(db_service_bulletin)  # add recall to the db
                db.session.commit()


if __name__ == "__main__":
    update_recalls()
    update_service_bulletins()
