from flask import Blueprint

from .login import Login
from .info import Info
from .logout import Logout

userapi = Blueprint('userapi',__name__)