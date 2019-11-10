#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
user = 'postgres'
password = '123'
host = 'db'
database = 'postgres'
port = '5432'
SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'