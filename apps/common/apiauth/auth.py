from flask import abort, session,jsonify,make_response
def user_auth(f):
    def decode(*args, **kwargs):
        if not session.get("_id"):
            return make_response(jsonify({"message":"未认证用户"}),401)
        return f(*args,**kwargs)
    return decode