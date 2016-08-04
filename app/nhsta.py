import requests

# http://www.nhtsa.gov/webapi/api/Recalls/vehicle/modelyear/2000/make/saturn/model/LS?format=json

#  Approach A. Get by Model Year, Make, Model

def get_all_model_years():
    pass

def get_all_makes_by_model_year():
    pass

def get_all_makes():
    pass

def get_recalls(model_year, make, model):
    """
    Queries NHTSA api for recall information.

    :param model_year: (int)
    :param make: (String)
    :param model: (String)
    :return:
    """
    api_url = 'http://www.nhtsa.gov/webapi/api/Recalls/vehicle/modelyear/{}/make/{}/model/{}?format=json'\
        .format(model_year, make, model)
    r = requests.get(api_url).json()
    assert r['Message'] == 'Results returned successfully', 'Bad response from nhtsa API.'
    return r['Results']

def lookup_vin(vin_number):
    pass

if __name__ == "__main__":
    model_year = 2000
    make = 'Honda'
    model = 'civic'
    recalls = get_recalls(model_year, make, model)
    print recalls
