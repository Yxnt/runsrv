from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_restful import Api, HTTPException
from flask_assets import Environment
from collections import OrderedDict
from apps.common import config
from apps.common.assest.assest import bundles
from apps.common.assest import assest

from json import dumps
from celery import Celery
import os

celery = Celery(__name__, broker=config[os.environ.get('FLASK_CONFIG') or 'dev'].CELERY_BROKER_URL,
                backend=config[os.environ.get('FLASK_CONFIG') or 'dev'].CELERY_RESULT_BACKEND)

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


def save_redis(message_code, message, **kwargs):
    mes = OrderedDict()
    mes['status'] = message_code
    mes['data'] = {"message": message}
    mes['data'].update(kwargs)

    return dumps(mes)


def create_apps(config_name):
    apps = Flask(__name__)
    apps.config.from_object(config[config_name])

    db.init_app(apps)

    assets.init_app(apps)
    assets.register(bundles)

    login.init_app(apps)
    login.login_view = 'userview.login'
    login.login_message = u"Before operation, please login"
    login.login_message_category = "info"
    login.session_protection = "strong"

    # Blueprint_view
    from apps.views import userview
    from apps.views import dashboard
    from apps.views import assetsview
    apps.register_blueprint(userview, url_prefix='/user')
    apps.register_blueprint(dashboard)
    apps.register_blueprint(assetsview, url_prefix='/dashboard')

    @apps.errorhandler(404)  # 404 处理
    def not_found(error):
        return RessourceDoesNotExist()

    @apps.before_first_request
    def init():
        apps.salt.login()

    with apps.app_context():
        from apps.models import User
        from apps.resources import userapi, Login, Info, Logout, saltapi, Minions

        api.init_app(userapi)
        # RestFul
        api.add_resource(Login, '/user/login')
        api.add_resource(Logout, '/user/logout')
        api.add_resource(Info, '/user/info/', '/user/info/<username>')
        api.add_resource(Minions, '/minions', '/minions/<minion>')

        # Blueprint
        apps.register_blueprint(userapi, url_prefix='/api')
        apps.register_blueprint(saltapi, url_prefix='/api')

        db.Model.metadata.reflect(bind=db.engine, schema='runsrv')

        apps.User = User
        apps.make_res = make_res
        apps.error = custom_error
        apps.save_redis = save_redis

        from apps.common.salt.salt import SaltApi
        from apps.common import Redis

        redis = Redis(ip=apps.config.get('REDIS_HOST'),
                      port=apps.config.get('REDIS_PORT'),
                      db=apps.config.get('REDIS_DB'),
                      password=apps.config.get('REDIS_AUTH'))

        s = SaltApi(user=apps.config.get('SALT_USER'),
                    passwd=apps.config.get('SALT_PASS'),
                    host=apps.config.get('SALT_HOST'),
                    port=apps.config.get('SALT_PORT'),
                    eauth=apps.config.get('SALT_EAUTH'),
                    is_ssl=apps.config.get('SALT_SSL_ON')
                    )

        apps.redis = redis
        apps.salt = s

    return apps
