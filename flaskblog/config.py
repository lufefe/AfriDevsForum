import os
import json

with open('/etc/config.json') as config_file:
	config = json.load(config_file)


class Config:
    SECRET_KEY = config.get('SECRET_KEY') # set in Environment Variables in Control Panel
    SQLALCHEMY_DATABASE_URI = config.get('SQLALCHEMY_DATABASE_URI') # database location | set in Environment Variables in Control Panel

    # for sending email for forgot password
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = config.get('EMAIL_USER') # set in Environment Variables in Control Panel
    MAIL_PASSWORD = config.get('EMAIL_PASS') # set in Environment Variables in Control Panel
