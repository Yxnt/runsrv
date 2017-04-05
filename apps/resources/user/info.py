from flask_restful import Resource, reqparse, abort
from flask import current_app
from collections import OrderedDict
from json import dumps

parse = reqparse.RequestParser()


class Info(Resource):
    data_dict = OrderedDict()
    user = []
    user_list = []

    def get(self, username=None):
        """获取用户接口
        :param username: 要查询的用户名
        :return: data_dict
        """
        if username != None:
            return self.__get_user(username)
        else:
            return current_app.make_error(500, 201, "接口异常")

    def __get_user(self, username):
        """获取用户方法
        :param username: 要查询的用户名
        :return: data_dict
        """
        user_info_dict = OrderedDict()
        self.user = current_app.User.query.all()

        if len(self.user) > 0:
            self.data_dict['status'] = "200"
            self.user_list.clear()
            for i in self.user:
                if username == i.username:
                    user_info_dict['user'] = i.username
                    user_info_dict['status'] = i.status
                    self.user_list.append(user_info_dict)
                    self.data_dict["data"] = self.user_list
                    return dumps(self.data_dict)
            return current_app.make_error(500, 201, "接口异常")
        else:
            return current_app.make_error(500, 203, "接口异常")
