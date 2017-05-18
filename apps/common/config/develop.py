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
    DBUSER = 'test'
    DBPASS = 'TBsImCEdW9gOM'
    DBHOST = '10.19.80.15'
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
    SQLALCHEMY_POOL_SIZE = 30
    SQLALCHEMY_POOL_TIMEOUT = 120

    REMEMBER_COOKIE_DURATION = timedelta(hours=2)

    # saltstack settings
    LOGIN_TOKEN_NAME = 'salt:login'
    SALT_HOST = '10.19.80.12'
    SALT_USER = 'salt'
    SALT_PASS = '123'
    SALT_EAUTH = 'pam'
    SALT_PORT = 8000
    SALT_SSL_ON = False

    # redis settings
    REDIS_HOST = '10.19.80.12'
    REDIS_PORT = 6379
    REDIS_DB = 0
    REDIS_AUTH = 'Gmtj6KQjLmL1Q'

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
    OPENFALCON_QUERY_SERVER = '10.19.80.14'
    OPENFALCON_QUERY_PORT = 9966

    # openfalcon DB
    OPENFALCON_DB_ADDR='10.19.80.13'
    OPENFALCON_DB_PORT=3306
    OPENFALCON_DB_USER = 'root'
    OPENFALCON_DB_PASSWORD='HxKQ2Bv4oxUvHnBQ'
    OPENFALCON_DB_NAME='graph'

    # monitor_addr
    MONITOR_ADDR = '127.0.0.1:5002'