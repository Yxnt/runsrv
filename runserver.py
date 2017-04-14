#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
from apps import create_apps, db, models, celery
from apps.models import User
from flask_script import Manager
from apps.tasks import update_host_list_to_db, system_operator

app = create_apps(os.environ.get('FLASK_CONFIG') or 'dev')
app.app_context().push()
manager = Manager(app)


@manager.command
def create_db():
    """创建所有的表"""
    db.create_all()


@manager.command
def create_admin():
    admin = User('admin', '123', 'admin@example.com')
    db.session.add(admin)
    db.session.commit()


if __name__ == '__main__':
    manager.run()
