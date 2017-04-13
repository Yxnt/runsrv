from flask import Blueprint

dashboard = Blueprint('dashboard',__name__)

from apps.views.dashboard import view