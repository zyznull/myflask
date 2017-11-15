import os
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'mysql://root:Password@localhost:3306/myflask?charset=utf8mb4'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS  = False
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
MAIL_SERVER='smtp.qq.com'
MAIL_PORT=465
MAIL_USE_SSL=True
MAIL_USERNAME = '571841510'
MAIL_PASSWORD = 'zroaqvmjbdnlbbgf'
FLASKY_MAIL_SUBJECT_PREFIX = 'myflask'
FLASKY_MAIL_SENDER = '571841510@qq.com'


CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'