from apps.views.assets import assetsview
from flask import render_template, current_app


@assetsview.route('/host')
def Host():
    return render_template('assets/host.html',title="主机管理")


@assetsview.route('/group')
def Group():
    return render_template('assets/group.html', title="分组管理")