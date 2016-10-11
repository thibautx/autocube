from datetime import datetime

import requests


def get_all_years():
    api_url = 'http://www.nhtsa.gov/webapi/api/Recalls/vehicle?format=json'
    r = requests.get(api_url).json()
    results = r['Results']
    model_years = [entry['ModelYear'] for entry in results]
    model_years.remove('9999')
    return map(int, model_years)


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
    # assert r['Message'] == 'Results returned successfully', 'Bad response from nhtsa API.'
    r = r['Results']
    recalls = []
    for recall_raw in r:
        recall = {}
        recall['consequence'] = recall_raw['Conequence']
        recall['components'] = recall_raw['Component']
        recall['NHTSACampaignNumber'] = recall_raw['NHTSACampaignNumber']
        millis = float(recall_raw['ReportReceivedDate'].split('-')[0].split('(')[1])
        date = datetime.fromtimestamp(millis/1000.0)
        recall['date'] = date
        recalls.append(recall)

    return recalls

if __name__ == "__main__":
    make = 'honda'
    model = 'civic'
    year = 2012
    print len(get_recalls(year, make, model))

