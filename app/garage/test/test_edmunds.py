import unittest
from app.garage import edmunds
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=2)

class TestEdmunds(unittest.TestCase):

    def test_get_front_quarter_image(self):
        make = 'Honda'
        model = 'Civic'
        year = 2008

        pp.pprint(edmunds.get_front_quarter_image(make, model, year))