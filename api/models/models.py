#!/usr/bin/python

from datetime import datetime
from api.database.database import db
from api.config.auth import auth, jwt
from flask import g


class User(db.Model):
    # __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(length=80))
    password = db.Column(db.String(length=80))
    email = db.Column(db.String(length=80))
    created = db.Column(db.DateTime, default=datetime.utcnow)
    user_role = db.Column(db.String, default='user')

    def generate_token(self):
        return jwt.dumps({'email': self.email, 'admin': 0}).decode('utf-8')


    @staticmethod
    @auth.verify_token
    def verify_auth_token(token):
        g.user = None
        try:
            data = jwt.loads(token)
        except:
            return False
        if 'email' and 'admin' in data:

            g.user = data['email']
            g.admin = data['admin']
            print(data)
        return(data)
            #return True
        return False


class Blacklist(db.Model):

    # __tablename__ = 'Blacklist'
    id = db.Column(db.Integer, primary_key=True)
    refresh_token = db.Column(db.String(length=255))
    access_token = db.Column(db.String(length=255))

