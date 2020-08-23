# import flask
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from flaskblog.config import *

db = SQLAlchemy()  # new instance of a database
migrate = Migrate()
bcrypt = Bcrypt()  # new instance of bcrypt encryption for password on register
login_manager = LoginManager()  # new instance of LoginManager lib for handling user login sessions
login_manager.session_protection = 'strong'
login_manager.login_view = 'users.login'  # telling the extension where the login view is (login function in users/routes.py)
login_manager.login_message_category = 'info'
mail = Mail()
ckeditor = CKEditor()
bootstrap = Bootstrap()
moment = Moment()


def create_app(config_class = DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.config.get('WHOOSH_BASE')

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    ckeditor.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)

    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    from flaskblog.error_handler.handlers import errors
    app.register_blueprint(users)  # users is the Blueprint variable
    app.register_blueprint(posts)  # posts is the Blueprint variable
    app.register_blueprint(main)  # main is the Blueprint variable
    app.register_blueprint(errors)

    return app
