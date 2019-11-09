#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask_restful import Api

from api.handlers.UserHandlers import (Register)


def generate_routes(app):
    api = Api(app)
    api.add_resource(Register, '/app/auth/register')

