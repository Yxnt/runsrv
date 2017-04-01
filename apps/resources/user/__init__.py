from flask import Blueprint

from .login import Login
from .info import Info

user = Blueprint('user',__name__)