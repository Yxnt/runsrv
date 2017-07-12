from apps.views.assets import assetsview
from flask import render_template
from flask_login import login_required


@assetsview.route('/host')
@login_required
def Host():
    return render_template('assets/host.html',title="主机管理")


@assetsview.route('/group')
@login_required
def Group():
    return render_template('assets/group.html', title="分组管理")