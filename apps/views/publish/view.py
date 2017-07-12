from . import publish
from flask import render_template
from flask_login import login_required


@publish.route('/publish')
@login_required
def index():
    return render_template('publish/new.html',title='新项目发布')

@publish.route('/repoinfo')
@login_required
def repoinfo():
    return render_template('publish/info.html',title='项目信息')

@publish.route('/exists')
@login_required
def repo_update():
    return render_template('publish/exists.html',title='项目更新')