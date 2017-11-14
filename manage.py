#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''

"""
from app import db,app
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand   #载入migrate扩展

manager = Manager(app)
migrate = Migrate(app, db)  #注册migrate到flask
manager.add_command('db', MigrateCommand)   #在终端环境下添加一个db命令

if __name__ == '__main__':
    manager.run()