from apps.common.config import Config
from datetime import timedelta
import string


class DevelopMent(Config):
    """
    开发版本配置文件
    """
    DEBUG = True
    SECRET_KEY = string.printable
    BUNDLE_ERRORS = True

    # DB Setting
    DBUSER = 'mycat'
    DBPASS = 'Z07EVSI@A9zO=Cgs'
    DBHOST = '10.106.0.229'
    DBPORT = 3306
    DBNAME = 'runsrv'
    SQLALCHEMY_DATABASE_URI = ('mysql+pymysql://'
                               '{DBUSER}:{DBPASS}@'
                               '{DBHOST}:{DBPORT}/'
                               '{DBNAME}?charset=utf8'.format(
        DBUSER=DBUSER,
        DBPASS=DBPASS,
        DBHOST=DBHOST,
        DBPORT=DBPORT,
        DBNAME=DBNAME
    ))

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 10

    REMEMBER_COOKIE_DURATION = timedelta(hours=2)
    PROPAGATE_EXCEPTIONS = False

    # saltstack settings
    LOGIN_TOKEN_NAME = 'salt:login'
    SALT_HOST = '127.0.0.1'
    SALT_USER = 'salt'
    SALT_PASS = 'ijTzNXhuI4k3o'
    SALT_EAUTH = 'pam'
    SALT_PORT = 8000
    SALT_SSL_ON = False
    MINIONS_FILE_ROOT = '/var/cache/salt/master/minions'

    # redis settings
    REDIS_HOST = '10.106.0.210'
    REDIS_PORT = 6378
    REDIS_DB = 15
    REDIS_AUTH = 'OSNqveQ5DIyM'

    # celery
    CELERY_BROKER_URL = "redis://:{PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}".format(
        PASSWORD=REDIS_AUTH,
        REDIS_HOST=REDIS_HOST,
        REDIS_PORT=REDIS_PORT,
        REDIS_DB=REDIS_DB
    )
    CELERY_RESULT_BACKEND = "redis://:{PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}".format(
        PASSWORD=REDIS_AUTH,
        REDIS_HOST=REDIS_HOST,
        REDIS_PORT=REDIS_PORT,
        REDIS_DB=REDIS_DB
    )
    CELERY_TASK_SERIALIZER = 'json'

    # openfalcon Api
    OPENFALCON_QUERY_SERVER = '10.106.0.209'
    OPENFALCON_QUERY_PORT = 9966

    # openfalcon DB
    OPENFALCON_DB_ADDR='10.106.0.209'
    OPENFALCON_DB_PORT=3306
    OPENFALCON_DB_USER = 'root'
    OPENFALCON_DB_PASSWORD='HxKQ2Bv4oxUvHnBQ'
    OPENFALCON_DB_NAME='graph'

    # monitor_addr
    MONITOR_ADDR = '127.0.0.1:5002'

    # gitlab
    GITLAB_ADDR = 'https://git.higsq.com:8889'
    GITLAB_TOKEN_HEADER = {"PRIVATE-TOKEN":"CrzuPZsvM_1xG88Bui-q"}
    GITLAB_USER = 'root'
    GITLAB_PASSWORD = 'w.ceUwOoWVKP2'
