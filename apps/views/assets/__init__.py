from flask import Blueprint

assetsview = Blueprint('assetsview', __name__)

from . import view
