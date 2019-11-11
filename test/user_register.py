import json
import unittest
from app import create_app
from api.config.routes import generate_routes
from http import HTTPStatus
from api.database.database import db
from api.models.models import User, Blacklist


class TestMyRegisterApi(unittest.TestCase):

    def setUp(self):
        self.app = create_app('test')
        generate_routes(self.app)
        self.client = self.app.test_client()
        self.data_exist = {
            "username": "mj",
            "password": "123",
            "email": "mj@yahoo.com"
        }
        self.data_wrong_for_register = {
            "username": "majid",
            "password": "123",
        }

        self.data_for_register_success = {
            "username": "majidamiri",
            "password": "123qwe",
            "email": "m.amiri@jaaar.org",
        }

    def test_register_success(self):
        resp = self.client.post(path='app/auth/register', data=json.dumps(self.data_for_register_success),
                                content_type='application/json')
        self.assertEqual(resp.status_code, HTTPStatus.OK)
        self.assertEqual(resp.json['message'], 'registration completed')
        with self.app.app_context():
            User.query.filter(User.email == self.data_for_register_success.get('email')).delete()
            db.session.commit()

    def test_register_wrong_data(self):
        resp = self.client.post(path='app/auth/register', data=json.dumps(self.data_wrong_for_register),
                                content_type='application/json')
        self.assertEqual(resp.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(resp.json['message'], 'Username, password or email is empty')

    def test_register_already_exist(self):
        user = User(username=self.data_exist.get('username'), password=self.data_exist.get('password'),
                    email=self.data_exist.get('email'))
        with self.app.app_context():
            db.session.add(user)
            db.session.commit()
        resp = self.client.post(path='app/auth/register', data=json.dumps(self.data_exist),
                                content_type='application/json')
        with self.app.app_context():
            User.query.filter(User.email == self.data_exist.get('email')).delete()
            db.session.commit()
        self.assertEqual(resp.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(resp.json['message'], 'User Already exists')

    if __name__ == '__main__':
        unittest.main()
