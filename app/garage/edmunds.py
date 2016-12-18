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
    all_makes = [str(make['name']) for make in r['makes']]
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
    :return: (list of JSON)
    { u'active': True,
          u'address': { u'apartment': u'',
                        u'city': u'Chicago',
                        u'country': u'USA',
                        u'county': u'Cook',
                        u'latitude': 41.901994,
                        u'longitude': -87.631403,
                        u'stateCode': u'IL',
                        u'stateName': u'Illinois',
                        u'street': u'1100 N Clark St',
                        u'zipcode': u'60610'},
          u'contactInfo': { u'phone': u'(888) 709-3477',
                            u'website': u'http://www.fjhonda.com'},
          u'dealerId': u'5532',
          u'distance': 1.298797419911752,
          u'fiveStarAwardYears': u'2016',
          u'name': u'Fletcher Jones Honda',
          u'niceName': u'FletcherJonesHonda',
          u'operations': { u'Friday': u'09:00 AM-06:00 PM',
                           u'Monday': u'09:00 AM-08:00 PM',
                           u'Saturday': u'09:00 AM-06:00 PM',
                           u'Sunday': u'Day off',
                           u'Thursday': u'09:00 AM-08:00 PM',
                           u'Tuesday': u'09:00 AM-08:00 PM',
                           u'Wednesday': u'09:00 AM-08:00 PM'},
          u'reviews': { u'sales': { u'count': 57,
                                    u'notRecommendedCount': 4,
                                    u'overallRating': 4.238,
                                    u'recommendedCount': 17},
                        u'service': { u'count': 71,
                                      u'notRecommendedCount': 2,
                                      u'overallRating': 4.755,
                                      u'recommendedCount': 47}},
          u'states': [u'USED', u'NEW'],
          u'type': u'ROOFTOP'
    }
    """
    api_url = 'https://api.edmunds.com/api/dealer/v2/dealers?zipcode={}&make={}&radius={}&fmt=json&api_key={}'\
        .format(zip, make, radius, API_KEY)
    r = requests.get(api_url).json()
    dealers = r['dealers']
    print len(dealers)
    for a in dealers:
        print a
    dealers = [format_dealer(dealer) for dealer in dealers]
    return dealers


def format_dealer(dealer):
    try:
        website = dealer['contactInfo']['website']
        phone = dealer['contactInfo']['phone']

    except KeyError:
        website = 'n/a'
        phone = 'n/a'

    dealer_formatted = {
        'name': dealer['name'],
        'address': format_dealer_address(dealer),
        'website': website,
        'phone': phone,
        'operations': dealer['operations'],
    }

    return dealer_formatted


def format_dealer_address(dealer):
    address = dealer['address']
    return '{}, {}, {} {}'.format(address['street'], address['city'], address['stateCode'], address['zipcode'])


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