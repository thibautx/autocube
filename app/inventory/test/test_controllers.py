import os
import app
import unittest
import tempfile
from flask import json
from app.database import init_db


class TestInventoryControllers(unittest.TestCase):

    def setUp(self):
        self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()
        with app.app.app_context():
            init_db()

    def test_api_makes(self):
        response = self.app.get('/inventory/api/makes')
        makes = json.loads(response.data)['makes']
        makes_expected = ['Lamborghini', 'Maserati']
        self.assertEqual(makes, makes_expected)

    def test_api_models(self):
        test_data = {'make': 'Lamborghini'}
        response = self.app.post('/inventory/api/models', data=test_data)
        models = json.loads(response.data)['models']
        expected_models = ['Aventador']
        self.assertEqual(models, expected_models)

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.app.config['DATABASE'])