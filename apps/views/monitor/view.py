from apps.views.monitor import monitor
from flask import render_template

@monitor.route('/graph')
def graph():
    return render_template('monitor/graph.html',title="监控图示")


@monitor.route('/screen')
def screen():
    return render_template('/')
