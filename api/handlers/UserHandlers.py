import logging
from datetime import datetime
import json
from flask import g, request, make_response, jsonify
from flask_restful import Resource
import api.error.errors as error
from api.database.database import db
from api.models.models import User, Blacklist
from api.config.auth import auth, refresh_jwt
from http import HTTPStatus


class Register(Resource):
    @staticmethod
    def post():
        try:
            username = request.json.get('username', '')
            password = request.json.get('password', '')
            email = request.json.get('email', '')
        except Exception as errorMessage:
            logging.info("Username, password or email is wrong.  %s." % errorMessage)
            return make_response(jsonify({
                'status': HTTPStatus.BAD_REQUEST,
                'message': 'Username, password or email is wrong',
            }), HTTPStatus.BAD_REQUEST)

        if email == '' or username == '' or password == '':
            return make_response(jsonify({
                'status': HTTPStatus.BAD_REQUEST,
                'message': 'Username, password or email is empty',
            }), HTTPStatus.BAD_REQUEST)

        user = User.query.filter_by(email=email).first()
        if user is not None:
            return make_response(jsonify({
                'status': HTTPStatus.BAD_REQUEST,
                'message': 'User Already exists',
            }), HTTPStatus.BAD_REQUEST)

        user = User(username=username, password=password, email=email)
        db.session.add(user)
        db.session.commit()
        return make_response(jsonify({
            'status': HTTPStatus.OK,
            'message': 'registration completed',
        }), HTTPStatus.OK)


class Login(Resource):
    @staticmethod
    def post():
        try:
            password = request.json.get('password', '')
            email = request.json.get('email', '')
        except Exception as errorMessage:
            logging.info("Username, password or email is wrong.  %s." % errorMessage)
            return make_response(jsonify({
                'status': HTTPStatus.BAD_REQUEST,
                'message': 'Username, password or email is wrong',
            }), HTTPStatus.BAD_REQUEST)

        if email == '' or password == '':
            return make_response(jsonify({
                'status': HTTPStatus.BAD_REQUEST,
                'message': 'password or email is empty',
            }), HTTPStatus.BAD_REQUEST)

        user = User.query.filter_by(email=email, password=password).first()
        if user is None:
            return make_response(jsonify({
                'status': HTTPStatus.BAD_REQUEST,
                'message': 'Username, password does not match',
            }), HTTPStatus.BAD_REQUEST)

        access_token = user.generate_token()

        refresh_token = refresh_jwt.dumps({'email': email}).decode('utf-8')
        return make_response(jsonify({
            'status': HTTPStatus.OK,
            'message': 'you are login now',
            'access_token': access_token,
            'refresh_token': refresh_token,
        }), HTTPStatus.OK)


class RefreshToken(Resource):
    @staticmethod
    def post():
        refresh_token = request.json.get('refresh_token')

        try:
            data = refresh_jwt.loads(refresh_token)

        except Exception as errorMessage:
            logging.error(errorMessage)
            return make_response(jsonify({
                'status': HTTPStatus.BAD_REQUEST,
                'message': 'refresh token is wrong'
            }), HTTPStatus.BAD_REQUEST)
        user = User.query.filter_by(email=data['email']).first()
        if user is None:

            return make_response(jsonify({
                'status': HTTPStatus.BAD_REQUEST,
                'message': 'refresh token is wrong'
            }), HTTPStatus.BAD_REQUEST)

        user = User(email=data['email'])
        token = user.generate_token()
        return make_response(jsonify({
            'status': HTTPStatus.OK,
            'message': 'refresh token done',
            'access_token': token,
        }), HTTPStatus.OK)


class Logout(Resource):
    @staticmethod
    def post():
        access_token = request.json.get('access_token')

        ref = Blacklist.query.filter_by(access_token=access_token, status=0).first()
        if ref is not None:
            return make_response(jsonify({
                'status': HTTPStatus.OK,
                'message': 'token is invalidated'
            }), HTTPStatus.OK)

        user_data = User.verify_auth_token(access_token)
        if not 'email' in user_data:
            return make_response(jsonify({
                'status': HTTPStatus.BAD_REQUEST,
                'message': 'access token is wrong'
            }), HTTPStatus.BAD_REQUEST)

        blacklist_refresh_token = Blacklist(access_token=access_token, status=0)
        db.session.add(blacklist_refresh_token)
        db.session.commit()
        return make_response(jsonify({
            'status': HTTPStatus.OK,
            'message': 'token is invalidated'
        }), HTTPStatus.OK)


class DataUserRequired(Resource):
    def get(self):
        access_token = request.json.get('access_token')
        ref = Blacklist.query.filter_by(access_token=access_token, status=0).first()
        if ref is not None:

            return make_response(jsonify({
                'status': HTTPStatus.BAD_REQUEST,
                'message': 'token is invalid'
            }), HTTPStatus.BAD_REQUEST)

        user_data = User.verify_auth_token(access_token)
        if 'email' in user_data:
            return make_response(jsonify({
                'status': HTTPStatus.OK,
                'message': 'your data is ready',
                'your email': user_data['email'],
            }), HTTPStatus.OK)

        return make_response(jsonify({
            'status': HTTPStatus.BAD_REQUEST,
            'message': 'token is invalid'
        }), HTTPStatus.BAD_REQUEST)

