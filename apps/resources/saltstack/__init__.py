from flask import Blueprint

from .minions import Minions
from .salt import Statesls, Git, LookJid, Cmd, File, FileDownload

saltapi = Blueprint('saltapi', __name__)
