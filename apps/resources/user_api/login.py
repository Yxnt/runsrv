# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse
from flask_login import login_user
from flask import current_app,request
from urllib import parse


class Login(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument('username', required=True, type=str, help="username error")
    parse.add_argument('password', required=True, type=str, help="password error")
    parse.add_argument('remeber', type=str)

    def post(self):
        args = self.parse.parse_args()
        username = args['username']
        password = args['password']
        remeber = args['remeber']

        user = current_app.User
        username = user.query.filter_by(username=username).first()
        if username:
            password = username.verify_password(password)
            if password:
                login_user(username, remeber)
        else:
            return current_app.make_res(500, 203, "登录失败，原因：账号或密码错误")

        url_query_column = parse.urlsplit(parse.unquote(request.referrer)).query
        if url_query_column:
            next_page = url_query_column.split('=')[1]
            return current_app.make_res(200,200,"登陆成功",next=next_page)

        else:
            return current_app.make_res(200,200,"登陆成功",next='/')