from flask import Flask


def create_apps():
    apps = Flask(__name__)
    apps.config.from_object('config')

    from apps.main import main as main_blueprint
    apps.register_blueprint(main_blueprint)

    return apps

