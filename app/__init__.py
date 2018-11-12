from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import os

from app.config import app_config

db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name):
    if os.getenv('FLASK_CONFIG') == "production":
        app = Flask(__name__)
        app.config.update(
            SECRET_KEY=os.getenv('SECRET_KEY'),
            SQLALCHEMY_DATABASE_URI=os.getenv('SQLALCHEMY_DATABASE_URI'),
            SQLALCHEMY_TRACK_MODIFICATIONS = False
        )
    else:
        app = Flask(__name__, instance_relative_config=True)
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config.from_object(app_config[config_name])
        #app.config.from_object('config.DevelopmentConfig')
        app.config.from_pyfile('config.py')
    
    Bootstrap(app)
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    migrate = Migrate(app, db)
    
    from app import models

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    from .errors import errors as errors_blueprint
    app.register_blueprint(errors_blueprint)

    return app
