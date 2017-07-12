from flask import Flask, request, redirect
from flask_login import LoginManager
from flask_restful import Api, HTTPException
from flask_assets import Environment
from flask_sqlalchemy import SQLAlchemy
from collections import OrderedDict
from apps.common import config
from apps.common.assest.assest import bundles
from apps.common.assest import assest

from celery import Celery
import os

celery = Celery(__name__, broker=config[os.environ.get('FLASK_CONFIG') or 'dev'].CELERY_BROKER_URL,
                backend=config[os.environ.get('FLASK_CONFIG') or 'dev'].CELERY_RESULT_BACKEND)

login = LoginManager()
api = Api()
assets = Environment()


class RessourceDoesNotExist(HTTPException):
    code = 404

    def get_body(self, environ=None):
        return "Page_Not_Found"


class ServerError(HTTPException):
    code = 500

    def get_body(self, environ=None):
        return "500"


def make_res(status_code, message_code, message, total=None, rows=None, **kwargs):
    """restful 接口返回信息"""
    mes = OrderedDict()
    mes['status'] = message_code
    mes['data'] = {"message": message}
    mes['data'].update(kwargs)
    mes['total'] = total
    mes['rows'] = rows

    return mes, status_code


def create_apps(config_name):
    apps = Flask(__name__)
    apps.config.from_object(config[config_name])

    assets.init_app(apps)
    assets.register(bundles)  # 初始化资源压缩

    login.init_app(apps)
    login.login_view = 'userview.login'  # 未登陆用户跳转
    login.login_message = u"Before operation, please login"
    login.login_message_category = "info"
    login.session_protection = "strong"

    # Blueprint_view
    from apps.views import userview
    from apps.views import dashboard
    from apps.views import assetsview
    from apps.views import system
    from apps.views import monitor
    from apps.views import publish
    from apps.views import cmd
    from apps.views import filemanager
    apps.register_blueprint(userview, url_prefix='/user')
    apps.register_blueprint(dashboard)
    apps.register_blueprint(assetsview, url_prefix='/dashboard')
    apps.register_blueprint(system, url_prefix='/dashboard')
    apps.register_blueprint(monitor, url_prefix='/dashboard')
    apps.register_blueprint(publish, url_prefix='/dashboard')
    apps.register_blueprint(cmd, url_prefix='/dashboard')
    apps.register_blueprint(filemanager, url_prefix='/dashboard')

    @apps.errorhandler(404)  # 404 处理
    def not_found(error):
        return RessourceDoesNotExist()

    @apps.errorhandler(500)
    def server_error(error):
        return ServerError()

    @apps.before_first_request
    def init():
        apps.salt.login()

    @apps.teardown_appcontext
    def shutdown_session(exception=None):
        if exception:
            from apps.models import session
            session.rollback()
            return

    with apps.app_context():
        from apps.resources import userapi, Login, Info, Logout, saltapi, Minions, Group, assetsapi
        from apps.resources import falcon, Query, monitorapi, Query_item, Report, gitrepo, GitInfo
        from apps.resources import Statesls, Git, LookJid, NgxLog, logstash_api, Cmd, GitTag, File
        from apps.resources import FileDownload

        api.init_app(userapi)
        # RestFul
        api.add_resource(Login, '/user/login')
        api.add_resource(Logout, '/user/logout')
        api.add_resource(Info, '/user/info/', '/user/info/<username>')

        api.add_resource(Minions, '/salt/minions/', '/salt/minions/<minion>')
        api.add_resource(Statesls, '/salt/state')
        api.add_resource(LookJid, '/salt/jid/')
        api.add_resource(Cmd, '/salt/cmd/')
        api.add_resource(File, '/salt/file/')
        api.add_resource(FileDownload, '/salt/file/download')

        api.add_resource(Group, '/assets/group/', '/assets/group/<groupname>')

        api.add_resource(Query, '/falcon/query/graph/<querypath>')
        api.add_resource(Query_item, '/falcon/endpoint_item/item/')

        api.add_resource(Report, '/monitor/report/')

        api.add_resource(GitInfo, '/publish/gitinfo/')
        api.add_resource(Git, '/publish/update/')
        api.add_resource(GitTag, '/publish/gittag/')

        api.add_resource(NgxLog, '/logstash/restime')

        # Blueprint
        apps.register_blueprint(userapi, url_prefix='/api')
        apps.register_blueprint(saltapi, url_prefix='/api')
        apps.register_blueprint(assetsapi, url_prefix='/api')
        apps.register_blueprint(falcon, url_prefix='/api')
        apps.register_blueprint(monitorapi, url_prefix='/api')
        apps.register_blueprint(gitrepo, url_prefix='/api')
        apps.register_blueprint(logstash_api, url_prefix='/api')

        apps.make_res = make_res

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

        # 初始化redis，saltstack
        apps.redis = redis
        apps.salt = s

    return apps
