import re
from datetime import datetime

from django.utils.text import slugify
from flask import current_app
# UserMixin is a class that we inherit from the required methods & attributes used in managing login sessions
from flask_login import UserMixin
# Serializer will be used for generating tokens for 'Forgot Password'
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from flaskblog import db, login_manager


def slugify(s):
    return re.sub('[^\w]+', '-', s).lower()


@login_manager.user_loader  # decorator used for reloading the user based on the user id stored in the session
def load_user(user_id):  # this function gets the user id
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):  # this class is used for creating the database table User
    id = db.Column(db.Integer, primary_key = True)  # id attribute/column that is an integer and primary key
    username = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    country = db.Column(db.String(20), nullable = False)
    image_file = db.Column(db.String(20), nullable = False, default = 'default.jpg')
    password = db.Column(db.String(60), nullable = True)
    posts = db.relationship('Post', backref = 'author',
                            lazy = True)  # defining a relationship between user(author) & post

    # author is a back reference which gives us access to the entire User model and the attributes
    # the posts variable will then be used in routes and views

    def get_reset_token(self, expires_sec = 1800):  # generates a token that will expire in 30 mins (1800 secs)
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)  # creates a serializer
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod  # tells python that this method won't have the 'self' object - it's a static method
    def verify_reset_token(token):  # verifies if token hasn't expired
        s = Serializer(current_app.config['SECRET_KEY'])  # creates a serializer
        try:
            user_id = s.loads(token)['user_id']  # tries to load the token to user_id
        except:
            return None  # returns None if token has expired
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


post_tag = db.Table('post_tag',
                    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
                    db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
                    )


class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    content = db.Column(db.Text, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)  # a foreign key

    tag = db.relationship('Tag', secondary = post_tag, backref = 'post', lazy = 'dynamic')

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64))
    slug = db.Column(db.String(64), unique = True)

    def __init__(self, *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)
        self.slug = slugify(self.name)

    def __repr__(self):
        return '<Tag %s>' % self.name
