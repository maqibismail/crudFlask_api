from flask_api import FlaskAPI
from flask import Blueprint
from flask.views import MethodView
from flask_sqlalchemy import SQLAlchemy
from flask import request, abort, make_response
from flask_restful import Resource, Api, reqparse
from flask_mysqldb import MySQL
from uuid import UUID
import os, base64
import uuid

# local import
from instance.config import app_config
candidate_blueprint = Blueprint('candidate', __name__)
db = SQLAlchemy()
candidate = ''

def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    from .models import Candidate, User
    from . import urls
    from .auth import auth_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(candidate_blueprint)
    
    return app