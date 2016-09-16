import json
import requests

API_TOKEN = 'UJuBHHwPxpEKKNQYafhtsKNHYDZb68FA'
ID = '43a21818-1988-41ba-90ee-38bd7063effd'
HEADERS = {
    'Timekit-App': 'autocube',
    'Content-type': 'application/json',
    'Accept': 'text/plain'
}


def register_user(user=None):
    api_url = 'https://api.timekit.io/v2/users'
    data = {
        'id': ID,
        # 'api_token': API_TOKEN,
        'email': 'test21470124047@gmail.com',
        'timezone': 'America/Chicago',
        'first_name': 'Thibaut',
        'password': 'abc123',

    }
    r = requests.post(api_url, data=json.dumps(data), headers=HEADERS)
    print r.text

def get_user_api_token(email):
    api_url = 'https://api.timekit.io/v2/auth'
    data = {
        'id': ID,
        'email': email,
        'password': 'abc123',
    }
    r = requests.post(api_url, data=json.dumps(data), headers=HEADERS).json()
    data = r['data']
    api_token = data['api_token']
    return api_token

def create_calendar():
    api_url = 'https://api.timekit.io/v2/calendars'
    data = {
        'name': 'test calendar',
        'description': 'test calendar description'
    }
    user = 'test21470124047@gmail.com'
    api_token = get_user_api_token(user)
    auth = (user, api_token)
    r = requests.post(api_url, data=json.dumps(data), auth=auth, headers=HEADERS).json()
    return r

if __name__ == "__main__":
    # register_user()
    # print get_user_api_token()
    print create_calendar()