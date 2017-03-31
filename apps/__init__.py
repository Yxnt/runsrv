from flask import Flask
from apps.common import config

from apps.views import hello


apps = Flask(__name__)

def create_apps(config_name):

    apps.config.from_object(config[config_name])

    with apps.app_context():
        apps.register_blueprint(hello)

    return apps

