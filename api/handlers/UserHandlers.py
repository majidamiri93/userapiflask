#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
from datetime import datetime
import json
from flask import g, request
from flask_restful import Resource

import api.error.errors as error
from api.database.database import db
from api.models.models import User, Blacklist
from api.config.auth import auth, refresh_jwt


class Register(Resource):
    @staticmethod
    def post():

        try:
            username, password, email = request.json.get('username').strip(), request.json.get('password').strip(), \
                                        request.json.get('email').strip()
        except Exception as why:
            logging.info("Username, password or email is wrong. " + str(why))
            return error.INVALID_INPUT_422

        if username is None or password is None or email is None:
            return error.INVALID_INPUT_422
        user = User.query.filter_by(email=email).first()
        if user is not None:
            return error.ALREADY_EXIST
        user = User(username=username, password=password, email=email)
        db.session.add(user)
        db.session.commit()
        return {'status': 'registration completed.'}


class Login(Resource):
    @staticmethod
    def post():
        try:
            email, password = request.json.get('email').strip(), request.json.get('password').strip()
        except Exception as why:
            logging.info("Email or password is wrong. " + str(why))
            return error.INVALID_INPUT_422

        if email is None or password is None:
            return error.INVALID_INPUT_422
        user = User.query.filter_by(email=email, password=password).first()
        if user is None:
            return error.DOES_NOT_EXIST
        if user.user_role == 'user':
            access_token = user.generate_token()
        else:
            return error.INVALID_INPUT_422
        refresh_token = refresh_jwt.dumps({'email': email}).decode('utf-8')
        return {'access_token': access_token, 'refresh_token': refresh_token}


class Logout(Resource):
    @staticmethod
    def post():
        refresh_token = request.json.get('refresh_token')
        access_token_be = request.json.get('Authorization').split()
        access_token = access_token_be[1]
        ref = Blacklist.query.filter_by(refresh_token=refresh_token).first()
        if ref is not None:
            return {'status': 'already invalidated', 'refresh_token': refresh_token}
        blacklist_refresh_token = Blacklist(refresh_token=refresh_token, access_token=access_token)
        db.session.add(blacklist_refresh_token)
        db.session.commit()
        return {'status': 'invalidated', 'refresh_token': refresh_token}


class DataUserRequired(Resource):

    def get(self):
        data = request.json.get('Authorization').split()
        access_token = data[1]
        ref = Blacklist.query.filter_by(access_token=access_token).first()
        if ref is not None:
            return {'status': 'invalid token', 'access_token': access_token}
        user_data = User.verify_auth_token(access_token)
        return {'state': 'success', 'email': user_data['email']}
