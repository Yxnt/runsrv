from flask import render_template
from flask_login import login_required
from . import filemanager


@filemanager.route('/file/upload')
@login_required
def upload():
    return render_template('filemanager/upload.html', title="文件上传")


@filemanager.route('/file/download')
@login_required
def download():
    return render_template('filemanager/download.html', title='文件下载')
