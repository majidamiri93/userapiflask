#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask_restful import Api

from api.handlers.UserHandlers import (Register, Login, Logout, DataUserRequired)


def generate_routes(app):
    api = Api(app)
    api.add_resource(Register, '/app/auth/register')
    api.add_resource(Login, '/app/auth/login')
    api.add_resource(Logout, '/app/auth/logout')
    api.add_resource(DataUserRequired, '/data_user')