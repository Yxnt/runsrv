from apps.common.config import Config
from datetime import timedelta
import string


class DevelopMent(Config):
    DEBUG = True
    SECRET_KEY = string.printable

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