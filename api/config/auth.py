#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask_httpauth import HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer as JWT

jwt = JWT('main', expires_in=3600)
refresh_jwt = JWT('refresh', expires_in=7200)
auth = HTTPTokenAuth('Bearer')
