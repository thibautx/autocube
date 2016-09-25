import json
import requests
from app.appointments.models import TimeKitUser

API_TOKEN = 'UJuBHHwPxpEKKNQYafhtsKNHYDZb68FA'
ID = '43a21818-1988-41ba-90ee-38bd7063effd'
HEADERS = {
    'Timekit-App': 'autocube',
    'Content-type': 'application/json',
    'Accept': 'text/plain'
}

def create_from_user(user):
    timekit_user = TimeKitUser(app_id=ID,
                               email=user.email,
                               password='abc123',
                               timezone='America/Chicago')
    user.timekit_user.append(timekit_user)

def _generate_password():
    pass


def register_user(user):
    """

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
        'password': user.timekit_user[0].password,
    }
    r = requests.post(api_url, data=json.dumps(data), headers=HEADERS).json()
    data = r['data']
    api_token = data['api_token']
    return api_token


def create_calendar(user, name=None, description=None):
    api_url = 'https://api.timekit.io/v2/calendars'
    data = {
        'name': 'test calendar',
        'description': 'test calendar description'
    }
    api_token = auth_user(user)
    auth = (user, api_token)
    r = requests.post(api_url, data=json.dumps(data), auth=auth, headers=HEADERS).json()
    return r

if __name__ == "__main__":
    # register_user()
    # print get_user_api_token()
    print create_calendar()