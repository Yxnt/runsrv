from flask import Blueprint

filemanager = Blueprint('filemanager',__name__)

from . import view