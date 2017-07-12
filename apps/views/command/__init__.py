from flask import Blueprint



cmd = Blueprint('cmd',__name__)

from . import view