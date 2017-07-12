from flask import Blueprint

from .info import GitInfo,GitTag

gitrepo = Blueprint('gitrepo',__name__)
