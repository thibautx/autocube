import json
import requests

# http://www.nhtsa.gov/webapi/api/Recalls/vehicle/modelyear/2000/make/saturn/model/LS?format=json


def get_all_years():
    api_url = 'http://www.nhtsa.gov/webapi/api/Recalls/vehicle?format=json'
    r = requests.get(api_url).json()
    results = r['Results']
    model_years = [entry['ModelYear'] for entry in results]
    model_years.remove('9999')
    return map(int, model_years)

def get_all_model_years_local():
    f = json.loads('model_years.json')
    pass

def get_makes_by_year(model_year):
    # /api/Recalls/vehicle/modelyear/2000?format=json
    api_url = 'http://www.nhtsa.gov/webapi/api/Recalls/vehicle/modelyear/{}?format=json'\
        .format(model_year)
    r = requests.get(api_url).json()
    results = r['Results']
    makes = [entry['Make'] for entry in results]
    return makes

def get_models_by_make_and_year(year, make):
    #  /api/Recalls/vehicle/modelyear/2000/make/saturn?format=json
    api_url = 'http://www.nhtsa.gov/webapi/api/Recalls/vehicle/modelyear/{}/make/{}?format=json'\
        .format(year, make)
    r = requests.get(api_url).json()
    results = r['Results']
    models = [entry['Model'] for entry in results]
    return models


def get_recalls(year, make, model):
    """
    Queries NHTSA api for recall information.

    :param year: (int)
    :param make: (String)
    :param model: (String)
    :return:
    """
    api_url = 'http://www.nhtsa.gov/webapi/api/Recalls/vehicle/modelyear/{}/make/{}/model/{}?format=json'\
        .format(year, make, model)
    r = requests.get(api_url).json()
    assert r['Message'] == 'Results returned successfully', 'Bad response from nhtsa API.'
    return r['Results']

def lookup_vin(vin_number):
    pass

if __name__ == "__main__":
    model_year = 2000
    make = 'Honda'
    # model = 'civic'
    # years = get_all_years()
    # makes = get_makes_by_year(model_year)
    print get_models_by_make_and_year(model_year, make)
    # recalls = get_recalls(model_year, make, model)
