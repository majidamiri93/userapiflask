import json
import unittest
from app import create_app
from api.config.routes import generate_routes
from http import HTTPStatus
from api.database.database import db
from api.models.models import User, Blacklist


class TestUserData(unittest.TestCase):

    def setUp(self):
        self.app = create_app('test')
        generate_routes(self.app)
        self.client = self.app.test_client()
        self.data_exist = {
            "username": "ali",
            "password": "123",
            "email": "ali@yahoo.com"
        }
        self.data_wrong_refresh_token = {
            "refresh_token": "sad@#$4hjjhkjJjkgLJSADAS"
        }
        self.data_wrong_access_token = {
            "access_token": "sad@#$4hjjhkjJjkgLJSADASasasdadsada"
        }

    def test_access_token_expire(self):
        expire_token = Blacklist(access_token=self.data_wrong_access_token.get('access_token'), status=0)
        with self.app.app_context():
            db.session.add(expire_token)
            db.session.commit()
        resp = self.client.get(path='data_user', data=json.dumps(self.data_wrong_access_token),
                                content_type='application/json')
        self.assertEqual(resp.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(resp.json['message'], 'token is invalid')
        with self.app.app_context():
            Blacklist.query.filter(Blacklist.access_token == self.data_wrong_access_token.get('access_token')).delete()
            db.session.commit()



    def test_access_token_success(self):
        user = User(username=self.data_exist.get('username'), password=self.data_exist.get('password'),
                    email=self.data_exist.get('email'))
        with self.app.app_context():
            db.session.add(user)
            db.session.commit()
        resp = self.client.post(path='app/auth/login', data=json.dumps(self.data_exist),
                                content_type='application/json')
        valid_access_token = {
            'access_token': resp.json['access_token']
        }
        resp = self.client.get(path='data_user', data=json.dumps(valid_access_token),
                                content_type='application/json')
        self.assertEqual(resp.status_code, HTTPStatus.OK)
        self.assertEqual(resp.json['message'], 'your data is ready')
        with self.app.app_context():
            User.query.filter(User.email == self.data_exist.get('email')).delete()
            db.session.commit()