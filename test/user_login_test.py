import json
import unittest
from app import create_app
from api.config.routes import generate_routes
from http import HTTPStatus
from api.database.database import db
from api.models.models import User, Blacklist

class TestMyLoginApi(unittest.TestCase):

    def setUp(self):
        self.app = create_app('test')
        generate_routes(self.app)
        self.client = self.app.test_client()
        self.data_exist = {
            "username": "ali",
            "password": "123",
            "email": "ali@yahoo.com"
        }
        self.data_wrong = {
            "username": "ali",
            "password": "1234",
            "email": "ali@yahoo.com"
        }
        self.data_empty_field = {
            "username": "ali",
            "password": "",
            "email": "ali@yahoo.com"
        }

    def test_login_wrong_data(self):
        user = User(username=self.data_exist.get('username'), password=self.data_exist.get('password'),
                    email=self.data_exist.get('email'))
        with self.app.app_context():
            db.session.add(user)
            db.session.commit()
        resp = self.client.post(path='app/auth/login', data=json.dumps(self.data_wrong),
                                content_type='application/json')
        self.assertEqual(resp.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(resp.json['message'], 'Username, password does not match')
        with self.app.app_context():
            User.query.filter(User.email == self.data_exist.get('email')).delete()
            db.session.commit()

    def test_login_empty_data(self):
        user = User(username=self.data_exist.get('username'), password=self.data_exist.get('password'),
                    email=self.data_exist.get('email'))
        with self.app.app_context():
            db.session.add(user)
            db.session.commit()
        resp = self.client.post(path='app/auth/login', data=json.dumps(self.data_empty_field),
                                content_type='application/json')
        self.assertEqual(resp.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(resp.json['message'], 'password or email is empty')
        with self.app.app_context():
            User.query.filter(User.email == self.data_exist.get('email')).delete()
            db.session.commit()

    def test_login_success(self):
        user = User(username=self.data_exist.get('username'), password=self.data_exist.get('password'),
                    email=self.data_exist.get('email'))
        with self.app.app_context():
            db.session.add(user)
            db.session.commit()
        resp = self.client.post(path='app/auth/login', data=json.dumps(self.data_exist),
                                content_type='application/json')
        self.assertEqual(resp.status_code, HTTPStatus.OK)
        self.assertEqual(resp.json['message'], 'you are login now')
        with self.app.app_context():
            User.query.filter(User.email == self.data_exist.get('email')).delete()
            db.session.commit()