from flask import Blueprint

logstash_api = Blueprint('logstash_api',__name__)

from .ngxlog import NgxLog