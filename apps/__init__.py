from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_restful import Api, HTTPException
from flask_assets import Environment
from collections import OrderedDict
from apps.common import config
from apps.common.assest.assest import bundles
from apps.common.assest import assest
from apps.resources import userapi, Login, Info,Logout

db = SQLAlchemy()
login = LoginManager()
api = Api()
assets = Environment()


class RessourceDoesNotExist(HTTPException):
    code = 404

    def get_body(self, environ=None):
        return "Page_Not_Found"


class custom_error():
    pass


def make_res(status_code, message_code, message, **kwargs):
    mes = OrderedDict()
    mes['status'] = message_code
    mes['data'] = {"message": message}
    mes['data'].update(kwargs)

    return mes, status_code


def create_apps(config_name):
    apps = Flask(__name__)

    apps.config.from_object(config[config_name])
    db.init_app(apps)
    api.init_app(userapi)
    assets.init_app(apps)
    assets.register(bundles)

    login.init_app(apps)
    login.login_view = 'userview.login'
    login.login_message = u"Before operation, please login"
    login.login_message_category = "info"
    login.session_protection = "strong"

    # RestFul
    api.add_resource(Login, '/user/login')
    api.add_resource(Logout, '/user/logout')
    api.add_resource(Info, '/user/info/', '/user/info/<username>')

    # Blueprint
    apps.register_blueprint(userapi, url_prefix='/api')



    with apps.app_context():
        from apps.models import User
        db.Model.metadata.reflect(bind=db.engine, schema='runsrv')
        apps.User = User
        apps.make_res = make_res
        apps.error = custom_error

        # Blueprint_view
        from apps.views import userview
        from apps.views import dashboard
        apps.register_blueprint(userview, url_prefix='/user')
        apps.register_blueprint(dashboard)


    @apps.errorhandler(404)  # 404 处理
    def not_found(error):
        return RessourceDoesNotExist()

    return apps
