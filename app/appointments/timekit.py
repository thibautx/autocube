from app import db
import json
import requests
from sqlalchemy import func

API_TOKEN = 'UJuBHHwPxpEKKNQYafhtsKNHYDZb68FA'
ID = '43a21818-1988-41ba-90ee-38bd7063effd'
HEADERS = {
    'Timekit-App': 'autocube',
    'Content-type': 'application/json',
    'Accept': 'text/plain'
}


def register_user(user):
    """
    Register a (User) on Time Kit.

    :param user: (User)
    :return:
    """
    api_url = 'https://api.timekit.io/v2/users'
    data = {
        'id': ID,
        'email': user.email,
        'timezone': 'America/Chicago',
        'first_name': user.first_name,
    }
    if user.last_name:
        data['last_name'] = user.last_name

    r = requests.post(api_url, data=json.dumps(data), headers=HEADERS)
    return r.json()


def remove_user(user):
    """
    Workaround for deleting user by setting random information effectively deleting the user

    :param user:
    :return:
    """
    api_url = 'https://api.timekit.io/v2/users'
    data = {
        'id': ID,
        'email': user.email,
    }
    r = requests.put(api_url, data=json.dumps(data), headers=HEADERS)
    return r.json()


def get_user(user):
    api_url = 'https://api.timekit.io/v2/users/me'
    r = requests.get(api_url, headers=HEADERS)
    return r.json()


def auth_user(user):
    api_url = 'https://api.timekit.io/v2/auth'
    data = {
        'id': ID,
        'email': user.email,
        'password': user.timekit['password'],
    }
    r = requests.post(api_url, data=json.dumps(data), headers=HEADERS).json()
    data = r['data']
    api_token = data['api_token']
    return api_token


def create_calendar(user, name=None, description=None):
    api_url = 'https://api.timekit.io/v2/calendars'
    data = {
        'name': user.first_name + 'Calendar',
        'description': 'test calendar description'
    }
    api_token = auth_user(user)
    auth = (user.email, api_token)
    r = requests.post(api_url, data=json.dumps(data), auth=auth, headers=HEADERS).json()['data']
    # user.timekit['calendar_id'] = r['id']
    # calendar_id = r['id']
    # user.update().values(timekit=func.json_object_set_key('calendar_id', calendar_id))
    # db.session.commit()
    return r


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


def create_widget(user, name=None):
    api_url = 'https://api.timekit.io/v2/widgets'
    api_token = auth_user(user)
    data = {
        'name': user.first_name + 'Calendar',
        'slug': user.first_name.lower() + '-widget',
        'config': {
            'email': user.email,
            'calendar': user.timekit['calendar_id'],
            'apiToken': api_token
        }
    }
    auth = (user.email, api_token)
    r = requests.post(api_url, data=json.dumps(data), auth=auth, headers=HEADERS).json()['data']
    # widget_id = r['id']
    # user.timekit['widget_id'] = widget_id
    # db.session.commit()
    return r


if __name__ == "__main__":
    # register_user()
    # print get_user_api_token()
    print create_calendar()