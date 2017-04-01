from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_restful import Api
from apps.common import config
from apps.resources import user, Login, Info

db = SQLAlchemy()
login = LoginManager()
api = Api()


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
        apps.User = User
        db.Model.metadata.reflect(bind=db.engine, schema='runsrv')



    # RestFul
    api.add_resource(Login, '/ceshi')
    api.add_resource(Info, '/api/user/info')

    # Blueprint
    apps.register_blueprint(user)

    return apps
