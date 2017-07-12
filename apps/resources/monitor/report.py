from flask_restful import Resource, reqparse
from apps.models import Monitor, session
from apps.common.apiauth.auth import user_auth


class Report(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("limit", type=int, location='args')
    parser.add_argument('offset', type=int, location='args')
    parser.add_argument('order', type=str, location='args')

    decorators = [user_auth]
    def get(self):
        args = self.parser.parse_args()

        if args['offset']:
            page = args['offset'] / 10 + 1
        else:
            page = 1

        if args['limit']:
            limit = args['limit']
        else:
            limit = 10

        ret = {}

        ret['total'] = len(session.query(Monitor).all())
        ret['rows'] = []

        data = session.query(Monitor).order_by(Monitor.id.asc()).offset(page).limit(limit).all()
        for i in data:
            ret['rows'].append({
                "hostname": i.hostname,
                "message":i.message,
                "level":i.level,
                "type":i.type,
                "time":str(i.c_time),
                "status":i.operator
            })

            session.commit()
        return ret
