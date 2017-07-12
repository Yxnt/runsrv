from flask import request, current_app
from flask_restful import Resource
import time


class NgxLog(Resource):
    def get(self):
        now = time.strftime('%Y.%m.%d')
        if request.json['timeout_type'] == 'res':
            key = 'logstash-res-timeout-%s' % now
        elif request.json['timeout_type'] == 'page':
            key = 'logstash-page-timeout-%s' % now

        current_app.redis.lpushx(key, request.data)

        return
