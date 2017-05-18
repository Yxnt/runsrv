from flask import request
from functools import wraps

def require_auth(fun):
    @wraps(fun)
    def auth(*args, **kwargs):
        print(request.authorization)
        return fun(args,kwargs)
    return auth