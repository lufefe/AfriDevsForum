import json

import requests
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required

from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from flaskblog.users.utils import save_picture, send_reset_email, send_confirmation_email

try:
    r = requests.get('https://restcountries.eu/rest/v2/region/africa')
    countries = r.json()
except ValueError:
    with open('flaskblog\static\json\countries.json') as json_file:
        countries = json.load(json_file)

users = Blueprint('users', __name__)


@users.before_app_request
def before_request():
    # user = User.query.get(3)
    # db.session.delete(user)
    # db.session.commit()
    if current_user.is_authenticated:
        if not current_user.confirmed \
                and request.endpoint \
                and request.blueprint != 'users' \
                and request.endpoint != 'static':
            return redirect(url_for('users.unconfirmed'))


@users.route("/unconfirmed")
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.home'))
    return render_template('unconfirmed.html')


@users.route("/register", methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RegistrationForm()
    form.country.choices = [(i['name'], i['name']) for i in countries]

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email = form.email.data, country = form.country.data,
                    password = hashed_password)
        db.session.add(user)
        db.session.commit()
        send_confirmation_email(user)
        flash('A confirmation email has been sent to you by email.', 'info')
        # flash('Your account has been created! You are now able to log in',
        #     'success')  # messages that pop up, 'success' is used for bootstrap
        return redirect(url_for('users.login'))
    return render_template('register.html', title = 'Register', form = form)


@users.route("/login", methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            next_page = request.args.get('next')  # gets the 'next 'parameter(s) from url if it exists
            return redirect(next_page) if next_page else redirect(
                url_for('main.home'))  # ternary condition for next_page
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title = 'Login', form = form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account", methods = ['GET', 'POST'])
@login_required  # decorator to tell the user must be logged in in order to access the account page/view
def account():
    form = UpdateAccountForm()
    form.country.choices = [(i['name'], i['name']) for i in countries]

    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data  # update the current user's username with the one if form
        current_user.email = form.email.data
        current_user.country = form.country.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.country.data = current_user.country
    image_file = url_for('static', filename = 'profile_pics/' + current_user.image_file)
    return render_template('account.html', title = 'Account', image_file = image_file, form = form)


# for viewing posts by selected user
@users.route("/user/<string:username>")
@login_required
def user_posts(username):
    page = request.args.get('page', 1, type = int)
    user = User.query.filter_by(username = username).first_or_404()
    # breaking the objects into multiple lines by putting a backslash before the (.)
    posts = Post.query.filter_by(author = user) \
        .order_by(Post.date_posted.desc()) \
        .paginate(page = page, per_page = 5)
    return render_template('user_posts.html', posts = posts, user = user)


@users.route("/reset_password", methods = ['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title = 'Reset Password', form = form)


@users.route("/reset_password/<token>", methods = ['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in',
              'success')  # messages that pop up, 'suucess' is used for bootstrap
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title = 'Reset Password', form = form)


@users.route("/confirm/<token>", methods = ['GET', 'POST'])
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.home'))
    if current_user.confirm(token):
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    else:
        flash('The confirmation link is invalid or has expired.', 'warning')
    return redirect(url_for('main.home'))


@users.route('/confirm')
@login_required
def resend_confirmation():
    send_confirmation_email(current_user)
    flash('A new confirmation email has been sent to you by email.', 'success')
    return redirect(url_for('users.login'))
