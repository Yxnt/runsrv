from flask_login import login_required

from apps.views.dashboard import dashboard


@dashboard.route('/')
@login_required
def index():
    return "2"