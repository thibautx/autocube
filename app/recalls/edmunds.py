import pprint
import requests

API_KEY = 'jv8tyz4h2twjq3ygqckkrzqa'

def get_makes():
    api_url = 'http://api.edmunds.com/api/vehicle/v2/makes?fmt=json&api_key={}'\
        .format(API_KEY)
    r = requests.get(api_url).json()
    all_makes = [make['name'] for make in r['makes']]
    return all_makes

def get_models(make):
    api_url = 'https://api.edmunds.com/api/vehicle/v2/{}/models?fmt=json&api_key={}'\
        .format(make, API_KEY)
    r = requests.get(api_url).json()
    all_models = [model['name'] for model in r['models']]
    return all_models

def get_model_years(make, model):
    api_url = 'http://api.edmunds.com/api/vehicle/v2/{}/{}/years?fmt=json&api_key={}'\
        .format(make, model, API_KEY)
    r = requests.get(api_url).json()
    model_years = [model_year['year'] for model_year in r['years']]
    return model_years

def get_image(make, model, year):
    api_url = 'https://api.edmunds.com/api/media/v2/{}/{}/{}/photos?fmt=json&api_key={}'\
        .format(make, model, year, API_KEY)
    r = requests.get(api_url).json()
    return r

def get_dealers(zip, make, radius=50):
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


if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=4)
    # listings = get_listings(61820)
    # print listings
    # pp.pprint(get_listings(61820))
    # print get_dealers(60601, 'Honda')
    # all_makes = get_all_makes()
    # all_models = get_models('Honda')
    model_years = get_model_years('Honda', 'Civic')
    print model_years
    # pp.pprint(all_models['models'][0]['name'])
    img = get_image('honda', 'civic', 2012)
    print img