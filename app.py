from flask import Flask, jsonify
import os

from api.config.config import SQLALCHEMY_DATABASE_URI
from api.config.config_test import SQLALCHEMY_DATABASE_URI_TEST
from api.config.routes import generate_routes
from api.database.database import db
from flask_swagger_ui import get_swaggerui_blueprint
from api.models.models import User
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


def create_app(mode: 'main'):
    app = Flask(__name__)
    app.config['DEBUG'] = True
    if mode == 'main':
        app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI_TEST
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)
    with app.app_context():
        db.create_all()
    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.json'
    SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Seans-Python-Flask-REST-Boilerplate"
        }
    )
    app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

    return app


if __name__ == '__main__':
    app = create_app('main')
    generate_routes(app)
    app.run(port=5000, debug=True, host='0.0.0.0')


