from flask_login import login_required

from apps.views.monitor import monitor
from flask import render_template

@monitor.route('/graph')
@login_required
def graph():
    return render_template('monitor/graph.html',title="监控图示")


# @monitor.route('/screen')
# def screen():
#     return render_template('/')


@monitor.route('/health')
@login_required
def health():
    return render_template('monitor/health.html',title="主机健康状态")

@monitor.route('/report')
@login_required
def report_manager():
    return render_template('monitor/report.html', title="告警管理")