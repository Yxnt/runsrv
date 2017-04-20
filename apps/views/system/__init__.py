from flask import Blueprint

system = Blueprint('system',__name__)

from apps.views.system import view