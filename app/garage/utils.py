import re
from app import db
from app.garage.models import Car, Recall, ServiceBulletin
from app.garage.edmunds import get_recalls, get_service_bulletins
from datetime import datetime


def on_new_car(car):
    """

    :param car:
    :return:
    """
    # car = Car.query.filter(Car.id == id).first()

    print car, type(car)

    make = car.make_no_space
    model = car.model_no_space
    year = car.year

    recalls = get_recalls(make, model, year)
    service_bulletins = get_service_bulletins(make, model, year)

    add_recalls(recalls, car)
    add_service_bulletins(service_bulletins, car)


def add_recalls(recalls, car):
    """

    :param recalls:
    :param car:
    :return:
    """

    for recall in recalls:
        recall_id = recall['id']
        manufactured_from, manufactured_to = _manufactured_to_and_from(recall)
        consequence = re.sub('([a-zA-Z])',
                             lambda x: x.groups()[0].upper(),
                             recall['defectConsequence'].lower(), 1)
        components = ', '.join(recall['componentDescription'].split(':'))
        db_recall = Recall(recall_id=recall_id,
                           nhtsa_number=recall['recallNumber'],
                           consequence=consequence,
                           components=components,
                           manufactured_from=manufactured_from,
                           manufactured_to=manufactured_to,
                           fixed=False,
                           date_fixed=None)

        car.recalls.append(db_recall)   # add recall to the car
        db.session.add(db_recall)       # add recall to the db
        db.session.commit()


def add_service_bulletins(service_bulletins, car):
    """

    :param service_bulletins:
    :param car:
    :return:
    """
    for service_bulletin in service_bulletins:
        service_bulletin_id = service_bulletin['id']
        bulletin_date = datetime.strptime(service_bulletin['bulletinDate'], "%Y-%m-%d").date()
        try:
            summary = re.sub('([a-zA-Z])',
                             lambda x: x.groups()[0].upper(),
                             service_bulletin['summaryText'].lower(), 1)
        except KeyError:
            continue  # skip if no summary

        db_service_bulletin = ServiceBulletin(service_bulletin_id=service_bulletin_id,
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


def _manufactured_to_and_from(recall):
    """
    Format manufactured to and from (from edmunds)

    :param recall:
    :return:
    """

    try:
        manufactured_from = datetime.strptime(recall['manufacturedFrom'], "%Y-%m-%d").date()
    except KeyError:
        manufactured_from = None
    try:
        manufactured_to = datetime.strptime(recall['manufacturedTo'], "%Y-%m-%d").date()
    except KeyError:
        manufactured_to = None

    return manufactured_from, manufactured_to