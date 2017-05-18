#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
from apps import create_apps, celery
from apps.models import User,session,Base
from flask_script import Manager
from apps.tasks import update_host_list_to_db, system_operator, redis_save, group_save, host_to_group
from apps.tasks import send_email

from celery.schedules import crontab


app = create_apps(os.environ.get('FLASK_CONFIG') or 'dev')  # 读取配置文件，优先从环境变量中获取配置
app.app_context().push()
manager = Manager(app)

# 定时计划
celery.conf.beat_schedule  = {
    'hostmonitor':{
        'task': 'apps.tasks.monitor.hostmonitor',
        'schedule':crontab()
    },
    'sendemail': {
        'task': 'apps.tasks.sender.email.send_email',
        'schedule': crontab()
    },
}



@manager.command
def create_db():
    """创建所有的表"""
    Base.metadata.create_all()


@manager.command
def create_admin():
    """初始化管理员账号"""
    admin = User('admin', '123', 'admin@example.com', status='enabled')
    session.add(admin)
    session.commit()


if __name__ == '__main__':
    manager.run()
