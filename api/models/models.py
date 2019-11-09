#!/usr/bin/python

from datetime import datetime
from api.database.database import db


class User(db.Model):

    # __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(length=80))
    password = db.Column(db.String(length=80))
    email = db.Column(db.String(length=80))
    created = db.Column(db.DateTime, default=datetime.utcnow)
    user_role = db.Column(db.String, default='user')

