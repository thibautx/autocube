import unittest
from app.garage import edmunds
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=2)

class TestEdmunds(unittest.TestCase):

    def test_get_models(self):
        make = 'BMW'
        # pp.pprint(edmunds.get_models(make))

    def test_get_image(self):
        make = 'BMW'
        model = '3Series'
        year = 2012

        pp.pprint(edmunds.get_image(make, model, year))

    def test_get_model_year_id(self):
        make = 'BMW'
        model = '3Series'
        year = 2012
        pp.pprint(edmunds.get_model_year_id(make, model, year))

    def test_get_recall(self):
        make = 'BMW'
        model = '3Series'
        # year =