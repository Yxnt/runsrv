from flask_login import login_required
from apps.views.dashboard import dashboard
from flask import render_template
from apps import celery


@dashboard.route('/')
@login_required
def index():
    tasks = len(celery.tasks.keys()) - 9
    return render_template('dashboard/index.html', title='仪表盘', counter=tasks)
