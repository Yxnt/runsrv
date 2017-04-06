from flask_login import login_required
from apps.views.dashboard import dashboard
from flask import render_template

@dashboard.route('/')
@login_required
def index():
    return render_template('dashboard/index.html', title='仪表盘')