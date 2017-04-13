from flask import Blueprint

assetsview = Blueprint('assetsview', __name__)

from apps.views.assets import view
