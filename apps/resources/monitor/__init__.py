from flask import Blueprint

from .item import Query_item
from .report import Report

monitorapi = Blueprint('monitorapi',__name__)

