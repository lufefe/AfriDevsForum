import os


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY')  #
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')  # database location
    FLASKY_COMMENTS_PER_PAGE = 3
    FLASKY_POSTS_PER_PAGE = 7
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    # for sending email for forgot password
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USER')  # set in Environment Variables in Control Panel
    MAIL_PASSWORD = os.environ.get('MAIL_PASS')  # set in Environment Variables in Control Panel


class ProductionConfig(Config):
    # with open('/etc/config.json') as config_file:
    # config = json.load(config_file)
    # SECRET_KEY = config.get('SECRET_KEY')  #
    # SQLALCHEMY_DATABASE_URI = config.get('SQLALCHEMY_DATABASE_URI')
    """Uses production database server."""


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
