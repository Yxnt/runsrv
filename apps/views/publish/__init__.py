from flask import Blueprint

publish = Blueprint('publish', __name__)

from . import view
