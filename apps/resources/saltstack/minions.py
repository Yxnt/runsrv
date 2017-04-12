from flask import current_app
from flask_restful import Resource


class Minions(Resource):
    def get(self,minion=None):
        if minion:
            return current_app.salt.minions(minion=minion)
        else:
            return current_app.salt.minions()