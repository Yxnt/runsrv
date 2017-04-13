from flask import Blueprint

userview = Blueprint('userview',__name__)

from apps.views.user import view