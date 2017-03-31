#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
from apps import create_apps
from flask_script import Manager

apps = create_apps(os.environ.get('FLASK_CONFIG') or 'dev')
manager = Manager(apps)

if __name__ == '__main__':
    manager.run()
