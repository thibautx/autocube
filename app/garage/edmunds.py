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
