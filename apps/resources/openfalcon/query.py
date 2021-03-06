from flask_restful import Resource, reqparse
from flask import current_app
from requests import post as _post
from json import dumps, loads
from apps.common.apiauth.auth import user_auth

class Query(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("start", type=int, location=["form", "json"])
    parser.add_argument("end", type=int, location=["form", "json"])
    parser.add_argument("cf", type=str, location=["form", "json"])
    parser.add_argument("endpoint_counters", type=str, location=["form", "json"])
    parser.add_argument("data",type=str,location=["form", "json"])
    parser.add_argument("endpoint", type=str, location=["form", "json"])
    parser.add_argument("counter", type=str, location=["form", "json"])
    decorators = [user_auth]
    def post(self, querypath):
        args = self.parser.parse_args()
        return self.falcon_query(querypath, args)

    def falcon_query(self, uri, data):
        query_addr = current_app.config.get("OPENFALCON_QUERY_SERVER")
        query_port = current_app.config.get("OPENFALCON_QUERY_PORT")
        query_service = "http://{}:{}/graph/{}".format(query_addr, query_port, uri)

        if uri == 'info' or uri == 'last':
            data = data['data']
        else:
            data.pop("endpoint")
            data.pop("counter")
            data.pop("data")
            data['endpoint_counters'] = loads(data['endpoint_counters'])
            data = dumps(data)

        response = _post(query_service, data=data, headers={"Content-Type": "application/json"})

        if response.status_code != 404:
            return response.json()
