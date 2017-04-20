from flask import Blueprint

from .minions import Minions

saltapi = Blueprint('saltapi', __name__)
