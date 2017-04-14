from flask import current_app
from flask_restful import Resource, reqparse
from apps.tasks import update_host_list_to_db, system_operator
from json import loads


class Minions(Resource):
    parse = reqparse.RequestParser()
    key = parse.add_argument('key', required=True, help="缺少key字段")
    name = parse.add_argument('name', required=True, help="缺少key字段")

    def get(self, minion=None):
        args = self.parse.parse_args()
        celery_metadata = current_app.redis.hget(args['name'], args['key'])
        celery_key = "celery-task-meta-%s" % celery_metadata.decode('utf-8')
        data = current_app.redis.get(celery_key).decode('utf-8')
        if data:
            return loads(data)['result']


    def post(self):
        operator = update_host_list_to_db.delay()
        system_operator.delay("update_host_list", operator.id)
        return current_app.make_res(200, 200, "执行成功", uuid=operator.id)
