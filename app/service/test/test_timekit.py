import unittest
import app.service.timekit as timekit
from app import db
# from app.profile.models import User
from app.service.models import Dealer
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=2)

class TestTimeKit(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_user = Dealer.query.filter(Dealer.email == 'thibaut@gmail.com')[0]

    def test_register_user(self):
        pp.pprint(timekit.register_user(self.test_user))

    def test_auth_user(self):
        api_token = timekit.auth_user(self.test_user)
        print api_token

    def test_create_calendar(self):
        pp.pprint(timekit.create_calendar(self.test_user))

    def test_get_calendar(self):
        print 'test get calendar'
        print timekit.get_calendar(self.test_user)

    def test_remove_user(self):
        # print timekit.remove_user(self.test_user)
        pass

    def test_get_user(self):
        print timekit.get_user(self.test_user)

    def test_get_user_api_token(self):
        pass

    def test_create_widget(self):
        pp.pprint(timekit.create_widget(self.test_user))

    def test_get_widget(self):
        print timekit.get_widget(self.test_user)