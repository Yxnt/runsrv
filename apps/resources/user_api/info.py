from flask_restful import Resource, reqparse
from flask import current_app
from collections import OrderedDict
from json import dumps
from apps.common.apiauth.auth import user_auth
from apps.models import User,session

parse = reqparse.RequestParser()


class Info(Resource):
    data_dict = OrderedDict()
    user = []
    user_list = []

    decorators = [user_auth]
    def get(self, username=None):
        """获取用户接口
        :param username: 要查询的用户名
        :return: data_dict
        """
        if username == None:
            userlen=len(session.query(User).all())
            session.commit()
            return current_app.make_res(200,200,"获取成功",counter=userlen)


    def __get_user(self, username):
        """获取用户方法
        :param username: 要查询的用户名
        :return: data_dict
        """
        user_info_dict = OrderedDict()
        self.user = session.query(User).all()

        if len(self.user) > 0:
            self.data_dict['status'] = "200"
            self.user_list.clear()
            for i in self.user:
                if username == i.username:
                    user_info_dict['user'] = i.username
                    user_info_dict['status'] = i.status
                    self.user_list.append(user_info_dict)
                    self.data_dict["data"] = self.user_list
                    session.commit()
                    return dumps(self.data_dict)
            session.commit()
            return current_app.make_res(500, 201, "接口异常")
        else:
            session.commit()
            return current_app.make_res(500, 203, "接口异常")
