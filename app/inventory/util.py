from app import db, Listing


def get_all_makes():
    """
    Get all makes.

    :param model:
    :return:
    """
    return sorted([row.make for row in db.session.query(Listing.make.distinct().label('make')).all()])


def get_all_models(make):
    """
    Get all the possible models by the make (sorted alphabetically)

    :param make: (str)
    :return: (list of str)
    """
    return sorted([row.model for row in db.session.query(Listing.model).filter(Listing.make == make).distinct().all()])