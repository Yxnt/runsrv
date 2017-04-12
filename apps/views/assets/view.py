from . import assetsview
from flask import render_template

@assetsview.route('/host')
def Host():
    return render_template('assets/host.html',title="主机管理")
