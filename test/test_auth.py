from unittest import TestCase

from app.instance import create_app, db
from config import DevelopmentTestingConfig


class TestAuthLogin(TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.app = create_app(DevelopmentTestingConfig())
        self.app.app_context().push()
        self.test_client = self.app.test_client()
        self.db = db

    def tearDown(self):
        self.db.connection.drop_database(self.app.config['MONGODB_SETTINGS']['DB'])

    def test_auth_index_response(self):
        with self.test_client.session_transaction():
            response = self.test_client.get('/')

        self.assertEqual(response._status_code, 200)

    def test_auth_google(self):
        with self.test_client.session_transaction() :
            response = self.test_client.get('/authorize/google')

        self.assertEqual(response._status_code, 302)
