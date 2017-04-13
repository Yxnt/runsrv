from apps.views.user import userview
from flask import render_template


@userview.route('/')
@userview.route('/login')
def login():
    return render_template('user/login.html', title="登陆")
