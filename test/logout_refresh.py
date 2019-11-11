import json
import unittest
from app import create_app
from api.config.routes import generate_routes
from http import HTTPStatus
from api.database.database import db
from api.models.models import User, Blacklist


class TestMyLogOut(unittest.TestCase):

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

    def test_wrong_access_token_for_logout(self):
        resp = self.client.post(path='app/auth/logout', data=json.dumps(self.data_wrong_access_token),
                                content_type='application/json')
        self.assertEqual(resp.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(resp.json['message'], 'access token is wrong')

    def test_valid_access_token_for_logout(self):
        user = User(username=self.data_exist.get('username'), password=self.data_exist.get('password'),
                    email=self.data_exist.get('email'))
        with self.app.app_context():
            db.session.add(user)
            db.session.commit()
        resp = self.client.post(path='app/auth/login', data=json.dumps(self.data_exist),
                                content_type='application/json')
        access_token = resp.json['access_token']
        valid_access_token = {
            'access_token': access_token
        }
        resp = self.client.post(path='app/auth/logout', data=json.dumps(valid_access_token),
                                content_type='application/json')
        self.assertEqual(resp.status_code, HTTPStatus.OK)
        self.assertEqual(resp.json['message'], 'token is invalidated')

        with self.app.app_context():
            User.query.filter(User.email == self.data_exist.get('email')).delete()
            db.session.commit()

    def test_wrong_refresh_token(self):
        resp = self.client.post(path='refresh_token', data=json.dumps(self.data_wrong_refresh_token),
                                content_type='application/json')
        self.assertEqual(resp.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(resp.json['message'], 'refresh token is wrong')

    def test_valid_refresh_token_with_login_first(self):
        user = User(username=self.data_exist.get('username'), password=self.data_exist.get('password'),
                    email=self.data_exist.get('email'))
        with self.app.app_context():
            db.session.add(user)
            db.session.commit()
        resp = self.client.post(path='app/auth/login', data=json.dumps(self.data_exist),
                                content_type='application/json')
        refresh_token = resp.json['refresh_token']
        valid_refresh_token = {
            'refresh_token': refresh_token
        }
        resp = self.client.post(path='refresh_token', data=json.dumps(valid_refresh_token),
                                content_type='application/json')
        self.assertEqual(resp.status_code, HTTPStatus.OK)
        self.assertEqual(resp.json['message'], 'refresh token done')

        with self.app.app_context():
            User.query.filter(User.email == self.data_exist.get('email')).delete()
            db.session.commit()
