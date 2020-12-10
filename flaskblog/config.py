from os import environ


class Config(object):
    # Config basics
    DEBUG = False
    TESTING = False
    SECRET_KEY = environ.get('SECRET_KEY')  #
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_TEST_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    WHOOSH_BASE = 'flaskblog/whoosh'

    # Email config
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = environ.get('MAIL_USER')
    MAIL_PASSWORD = environ.get('MAIL_PASS')

    # Blog parameters
    FLASKY_COMMENTS_PER_PAGE = 4
    FLASKY_POSTS_PER_PAGE = 7
    FLASKY_ADMIN = environ.get('FLASKY_ADMIN')
    MAX_SEARCH_RESULTS = 50


class ProductionConfig(Config):
    """ TODO --> Update config.json file on server :
       1. SQLALCHEMY_PROD_DATABASE_URI
       2. FLASK_ENV
    """
    # with open('/etc/config.json') as config_file:
    # config = json.load(config_file)
    # SECRET_KEY = config.get('SECRET_KEY')  #
    # SQLALCHEMY_DATABASE_URI = config.get('SQLALCHEMY_PROD_DATABASE_URI')
    # FLASK_ENV = 'production'
    """Uses production database server."""


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True

# config = {
#     'development': DevelopmentConfig,
#     'production': ProductionConfig,
#     'default': DevelopmentConfig
# }
