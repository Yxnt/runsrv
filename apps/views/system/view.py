from flask import render_template
from flask_login import login_required

from apps.views.system import system


@system.route('/system')
@login_required
def index():
    return render_template('system/index.html')
