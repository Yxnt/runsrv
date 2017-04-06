from flask_restful import Resource
from flask_login import logout_user
from flask import redirect, url_for


class Logout(Resource):
    def get(self):
        logout_user()
        return redirect(url_for('userview.login'))
