from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

def creat_app():
    app = Flask(__name__)
    app.config.from_object('config')
    db = SQLAlchemy(app)
    lm = LoginManager()
    lm.init_app(app)
    lm.login_view = '/login'
    mail = Mail()
    mail.init_app(app)
    return app

application = creat_app()

if __name__ == '__main__':
    application.run()

from app import views, models,email