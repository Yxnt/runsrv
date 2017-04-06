from flask import Blueprint

from .login import Login
from .info import Info

userapi = Blueprint('userapi',__name__)