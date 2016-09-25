from app import db
from app.profile.models import User
from app.appointments.models import TimeKitUser
import app.appointments.timekit as timekit
import unittest


class TestTimeKit(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_user = User.query.filter(User.email == 'txiong3@illinois.edu')[0]

    def test_register_user(self):
        print timekit.register_user(self.test_user)

    def test_auth_user(self):
        # add user
        timekit.create_from_user(self.test_user)
        api_token = timekit.auth_user(self.test_user)
        print api_token

    def test_create_calendar(self):
        pass

    def test_remove_user(self):
        # print timekit.remove_user(self.test_user)
        pass

    def test_get_user(self):
        print timekit.get_user(self.test_user)

    def test_get_user_api_token(self):
        pass
