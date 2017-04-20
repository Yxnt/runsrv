from flask import render_template
from apps.views.system import system


@system.route('/system')
def index():
    return render_template('system/index.html')
