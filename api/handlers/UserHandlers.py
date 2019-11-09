#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
from datetime import datetime

from flask import g, request
from flask_restful import Resource

import api.error.errors as error
from api.database.database import db
from api.models.models import User


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



