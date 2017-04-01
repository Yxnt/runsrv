from flask_restful import Resource, reqparse
from flask import current_app
from collections import OrderedDict
from json import dumps

parse = reqparse.RequestParser()


class Info(Resource):
    def get(self):
        data = OrderedDict()
        user = current_app.User.query.all()
        user_list = []
        if len(user) > 0:
            data['status'] = "success"
            for i in user:
                user_list.append({"username": i.username})
            data["data"] = user_list

        return dumps(data)
