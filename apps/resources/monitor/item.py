from apps.models.openfalcon import session, endpoint_counter, endpoint
from flask_restful import Resource, reqparse


class Query_item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('endpoint', type=str, location=["args"])

    def get(self):
        ret = []
        args = self.parser.parse_args()
        endpoint_name = args['endpoint']
        endpoint_id = session.query(endpoint).filter_by(endpoint=endpoint_name).first()
        if endpoint_id:
            for i in session.query(endpoint_counter).filter_by(endpoint_id=endpoint_id.id):
                ret.append(i.counter)
        session.commit()
        return ret
