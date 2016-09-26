from app import db
from app.profile.models import User
import app.appointments.timekit as timekit
import unittest


class TestTimeKit(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_user = User.query.filter(User.email == 'txiong3@illinois.edu')[0]

        timekit = {
            'app_id': '43a21818-1988-41ba-90ee-38bd7063effd',
            'email': cls.test_user.email,
            'timezone': 'America/Chicago',
            'first_name': cls.test_user.first_name,
            'password': 'abc123',
            'calendar_id': '44d0bc97-c6e0-4e4b-a4e7-0e1c7439976c',
            'widget_id': '5bb2d2f0-e0d9-4b4c-89de-3a098542b016',
        }

        # setattr(cls.test_user, 'timekit', timekit)
        #
        # makes_serviced = {
        #     'honda': 1
        # }
        #
        # setattr(cls.test_user, 'makes_serviced', makes_serviced)
        db.session.commit()

    def test_register_user(self):
        timekit.register_user(self.test_user)

    def test_auth_user(self):
        # add user
        api_token = timekit.auth_user(self.test_user)

    def test_create_calendar(self):
        print timekit.create_calendar(self.test_user)

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
        print timekit.create_widget(self.test_user)

    def test_get_widget(self):
        print timekit.get_widget(self.test_user)