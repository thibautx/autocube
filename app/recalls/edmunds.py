import pprint
import requests

API_KEY = 'jv8tyz4h2twjq3ygqckkrzqa'

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
    listings = get_listings(61820)
    print listings
    # pp.pprint(get_listings(61820))
    # print get_dealers(60601, 'Honda')