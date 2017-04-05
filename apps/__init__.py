from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_restful import Api, HTTPException
from collections import OrderedDict
from json import dumps
from apps.common import config
from apps.resources import user, Login, Info

db = SQLAlchemy()
login = LoginManager()
api = Api()


class RessourceDoesNotExist(HTTPException):
    code = 404

    def get_body(self, environ=None):
        return "Page_Not_Found"

class custom_error():
    pass

def make_error(status_code, message_code, message):
    mes = OrderedDict()
    mes['status'] = message_code
    mes['data'] = {"message": message}
    response = dumps(mes)
    return response, status_code


def create_apps(config_name):
    apps = Flask(__name__)

    apps.config.from_object(config[config_name])
    db.init_app(apps)
    api.init_app(user)

    login.init_app(apps)
    login.login_view = ''
    login.login_message = u"Before operation, please login"
    login.login_message_category = "info"
    login.session_protection = "strong"

    with apps.app_context():
        from apps.models import User
        db.Model.metadata.reflect(bind=db.engine, schema='runsrv')

        apps.User = User
        apps.make_error = make_error
        apps.error = custom_error

    # RestFul
    api.add_resource(Login, '/ceshi')
    api.add_resource(Info, '/user/info/', '/user/info/<username>')

    # Blueprint
    apps.register_blueprint(user, url_prefix='/api')

    @apps.errorhandler(404)
    def not_found(error):
        return RessourceDoesNotExist()

    return apps
