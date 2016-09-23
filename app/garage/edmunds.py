import requests

API_KEY = 'jv8tyz4h2twjq3ygqckkrzqa'


def get_makes():
    """
    All possible makes.

    :return: (list of str)
    """
    api_url = 'http://api.edmunds.com/api/vehicle/v2/makes?fmt=json&api_key={}'\
        .format(API_KEY)
    r = requests.get(api_url).json()
    all_makes = [make['name'] for make in r['makes']]
    return all_makes


def get_models(make):
    """
    All models for a certain make.

    :param make: (str)
    :return: (list of str)
    """
    api_url = 'https://api.edmunds.com/api/vehicle/v2/{}/models?fmt=json&api_key={}'\
        .format(make, API_KEY)
    r = requests.get(api_url).json()
    all_models = [model['name'] for model in r['models']]
    return all_models


def get_model_years(make, model):
    """
    Model years for a certain make/model.

    :param make: (str)
    :param model: (str)
    :return: (list of str)
    """
    api_url = 'http://api.edmunds.com/api/vehicle/v2/{}/{}/years?fmt=json&api_key={}'\
        .format(make, model, API_KEY)
    r = requests.get(api_url).json()
    model_years = [model_year['year'] for model_year in r['years']]
    return model_years


def get_model_year_id(make, model, year):
    api_url = 'https://api.edmunds.com/api/vehicle/v2/{}/{}/{}?fmt=json&api_key={}'\
        .format(make, model, year, API_KEY)
    r = requests.get(api_url).json()
    return r['id']


def get_recalls(make, model, year):
    model_year_id = get_model_year_id(make, model, year)
    api_url = 'https://api.edmunds.com/v1/api/maintenance/recallrepository/findbymodelyearid?modelyearid={}&fmt=json&api_key={}'\
        .format(model_year_id, API_KEY)
    r = requests.get(api_url).json()
    return r['recallHolder']


def get_service_bulletins(make, model, year):
    id = get_model_year_id(make, model, year)
    api_url = 'https://api.edmunds.com/v1/api/maintenance/servicebulletinrepository/findbymodelyearid?' \
              'modelyearid={}&fmt=json&api_key={}'\
        .format(id, API_KEY)
    r = requests.get(api_url).json()
    return r['serviceBulletinHolder']


def get_image(make, model, year):
    """

    :param make:
    :param model:
    :param year:
    :return:
    """
    api_url = 'https://api.edmunds.com/api/media/v2/{}/{}/{}/photos?fmt=json&api_key={}'\
        .format(make, model, year, API_KEY)
    r = requests.get(api_url).json()
    return r


def get_dealers(zip, make, radius=50):
    """
    Get dealers within a radius that service cars of a certain make.

    :param zip: (str/int)
    :param make: (str)
    :param radius: (int)
    :return:
    """
    api_url = 'https://api.edmunds.com/api/dealer/v2/dealers?zipcode={}&make={}&radius={}&fmt=json&api_key={}'\
        .format(zip, make, radius, API_KEY)
    r = requests.get(api_url).json()
    dealers = r['dealers']
    return dealers


def get_listings(zip):
    api_url = 'https://api.edmunds.com/api/inventory/v2/inventories?zipcode={}&fmt=json&api_key={}'\
        .format(zip, API_KEY)
    r = requests.get(api_url).json()
    return r


import pprint
if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=4)
    year = 2012
    make = 'Honda'
    model = 'Civic'
    r = get_service_bulletins(make, model, year)
    pp.pprint(r)