from flask import current_app
from flask_restful import Resource, reqparse
from apps.tasks import update_host_list_to_db, system_operator
from json import loads
from apps.models import Host
from apps.tasks import redis_save
from json import dumps


class Minions(Resource):
    parse = reqparse.RequestParser()
    key = parse.add_argument('key', required=True, help="缺少key字段")
    name = parse.add_argument('name', required=True, help="缺少key字段")

    def get(self, minion=None):
        args = self.parse.parse_args()
        celery_metadata = current_app.redis.hget(args['name'], args['key'])
        celery_key = "celery-task-meta-%s" % celery_metadata.decode('utf-8')

        if current_app.redis.get(celery_key):
            data = current_app.redis.get(celery_key).decode('utf-8')
            return loads(data)['result']
        else:
            client_number = len(Host.query.all())
            info = {}
            info['client_number'] = client_number
            info['clients'] = []

            for i in Host.query.all():
                info['clients'].append({"hostname": i.host_name,
                 "ip": i.host_ip,
                 "location":i.host_location,
                 "osinfo":i.host_os,
                 "status":i.host_stats,
                 "group":""})

            data = {
                "traceback": "null",
                "status": "SUCCESS",
                "children": [],
                "task_id": celery_metadata.decode('utf-8'),
                "result": info
            }
            redis_save.delay(celery_key,dumps(data))
            return info

    def post(self):
        operator = update_host_list_to_db.delay()
        system_operator.delay("update_host_list", operator.id)
        return current_app.make_res(200, 200, "执行成功", uuid=operator.id)
