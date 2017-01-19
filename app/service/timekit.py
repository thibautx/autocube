import json
import requests
import random
import string
from app import db
from app.service.models import Dealer
from sqlalchemy import func


def random_pass(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))

API_TOKEN = 'Lc1iP5Pkl9tAtNSi7x4GGxYpMmiaEMN0'  # global API token
APP_ID = 'fb67e90f-7491-44eb-82fd-5c58cd72c030' # autocube-dev app id
HEADERS = {
    'Timekit-App': 'autocube-dev',
    'Content-type': 'application/json',
    'Accept': 'text/plain'
}


def on_new_dealer(dealer):
    """
    When a dealer registers on Autoube,
    1) Register dealer on timekit.
    2) Create a new calendar for the dealer.
    :return:
    """

    # user registration
    register, timekit = register_user(dealer)

    # create a calendar
    calendar, timekit = create_calendar(dealer)

    # create widget
    widget, timekit = create_widget(dealer)

    return timekit


def register_user(dealer):
    """
    Register a (Dealer) on Time Kit.
    Save the "email" and "token" from the response for the next API requests

    :param dealer: (Dealer)
    :param password:
    :return:
    { u'data': { u'api_token': u'SVRidjcEM8ihovaJXM0qMrkn24k9RgO0',
             u'created_at': u'2016-10-11T18:24:36+0000',
             u'email': u'test@test.commm',
             u'first_name': u'test',
             u'id': u'e84e6bf0-16f6-4032-81fb-0eb0c623a6da',
             u'image': None,
             u'last_name': None,
             u'name': u'test ',
             u'timezone': u'America/Chicago',
             u'updated_at': u'2016-10-11T18:24:36+0000'}}
    """
    api_url = 'https://api.timekit.io/v2/users'
    password = random_pass(10)
    data = {
        'id': APP_ID,
        'email': dealer.email,
        'timezone': 'America/Chicago',
        'first_name': dealer.name,
        'password': password,
    }

    r = requests.post(api_url, data=json.dumps(data), headers=HEADERS).json()['data']
    api_token = r['api_token']
    id = r['id']
    timekit = {'api_token': api_token,
               'id': id,
               'password': password}

    dealer.timekit = timekit
    db.session.commit()
    return r, timekit


def remove_user(user):
    """
    Workaround for deleting user by setting random information effectively deleting the user

    :param user:
    :return:
    """
    api_url = 'https://api.timekit.io/v2/users'
    data = {
        'id': APP_ID,
        'email': user.email,
    }
    r = requests.put(api_url, data=json.dumps(data), headers=HEADERS)
    return r.json()


def get_user(user):
    api_url = 'https://api.timekit.io/v2/users/me'
    r = requests.get(api_url, headers=HEADERS)
    return r.json()


def auth_user(user):
    """

    :param user:
    :return:
    """
    api_url = 'https://api.timekit.io/v2/auth'
    print user.timekit['password']
    data = {
        'id': APP_ID,
        'email': user.email,
        'password': user.timekit['password'],
    }
    r = requests.post(api_url, data=json.dumps(data), headers=HEADERS).json()
    print r
    data = r['data']
    api_token = data['api_token']
    return api_token


def create_calendar(dealer, name=None, description=None):
    """

    :param dealer:
    :param name:
    :param description:
    :return:
    { u'backgroundcolor': None,
      u'created_at': u'2016-10-11T13:56:38-0500',
      u'description': u'test calendar description',
      u'foregroundcolor': None,
      u'id': u'4cf2cd45-9acd-45dc-999e-9610e9544da1',
      u'name': u'Thibaut DealershipCalendar',
      u'provider_access': u'owner',
      u'provider_id': None,
      u'provider_primary': False,
      u'provider_sync': False,
      u'updated_at': u'2016-10-11T13:56:38-0500'}
    """
    api_url = 'https://api.timekit.io/v2/calendars'
    data = {
        'name': dealer.name + 'Calendar',
        'description': 'test calendar description'
    }
    api_token = dealer.timekit['api_token']
    auth = (dealer.email, api_token)
    r = requests.post(api_url, data=json.dumps(data), auth=auth, headers=HEADERS).json()['data']

    timekit = dealer.timekit
    timekit['calendar_id'] = r['id']
    print 'before update', timekit
    db.session.query(Dealer).filter(Dealer.id == dealer.id).update({'timekit': timekit})
    db.session.commit()
    print 'updated dealer timekit', dealer.timekit
    return r, timekit


def get_calendar(user):
    """
    Get user's calendar-id

    :param user:
    :return:
    """
    api_url = 'https://api.timekit.io/v2/calendars/{}'.format(user.calender_id)
    api_token = auth_user(user)
    auth = (user.email, api_token)
    r = requests.get(api_url, auth=auth, headers=HEADERS).json()
    return r['data'][0]['id']


def create_widget(dealer, name=None):
    """

    :param dealer:
    :param name:
    :return:
     {
      "data": {
        "id": "826ddc8e-8698-45be-9320-0c81dcf797d9",
        "name": "My Test Widget",
        "slug": "my-test-widget",
        "config": {
          "email": "marty.mcfly@timekit.io",
          "calendar": "3653d9a9-46d3-4270-8d34-34b3d871128d",
          "apiToken": "xwcgiK7u7EZSpIkCSt3Oaq1eFy1fZBJA"
        }
      }
    }
    """
    api_url = 'https://api.timekit.io/v2/widgets'
    api_token = auth_user(dealer)
    data = {
        'name': dealer.name + 'Calendar',
        'slug': (dealer.name.lower() + '-widget').replace(" ", ""),
        'config': {
            'email': dealer.email,
            'calendar': dealer.timekit['calendar_id'],
            'apiToken': api_token
        }
    }
    auth = (dealer.email, api_token)
    # print data
    r = requests.post(api_url, data=json.dumps(data), auth=auth, headers=HEADERS).json()
    # print r
    r = r['data']
    timekit = dealer.timekit
    widget_id = r['id']
    widget_name = r['name']
    widget_slug = r['slug']
    timekit['widget_id'] = widget_id
    timekit['widget_name'] = widget_name
    timekit['widget_slug'] = widget_slug
    db.session.query(Dealer).filter(Dealer.id == dealer.id).update({'timekit': timekit})
    db.session.commit()
    return r, timekit


def get_widget(user):
    api_url = 'https://api.timekit.io/v2/widgets/embed/{}'.format(user.timekit['widget_id'])
    api_token = auth_user(user)
    auth = (user.email, api_token)
    r = requests.get(api_url, auth=auth, headers=HEADERS).json()['data']
    return r
