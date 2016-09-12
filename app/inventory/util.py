# from app import db
#
#
# def get_all_makes():
#     """
#     Get all makes.
#
#     :param model:
#     :return:
#     """
#     return sorted([row.make for row in db.session.query(Listing.make.distinct().label('make')).all()])
#
#
# def get_all_models(make):
#     """
#     Get all the possible models by the make (sorted alphabetically)
#
#     :param make: (str)
#     :return: (list of str)
#     """
#     return sorted([row.model for row in db.session.query(Listing.model).filter(Listing.make == make).distinct().all()])
#
#
# def get_all_listings():
#     all_listings = Listing.query.all()
#     return all_listings
#
#
# def get_listings_by_make(make):
#     listings = Listing.query.filter(Listing.make == make).all()
#     return listings
#
#
# def get_listings_by_make_model(make, model):
#     listings = Listing.query.filter(Listing.make == make).filter(Listing.model == model).all()
#     return listings