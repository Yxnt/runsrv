from . import cmd
from flask import render_template
from flask_login import login_required

@login_required
@cmd.route('/cmd')
def index():
    return render_template('command/index.html',title="命令执行")
