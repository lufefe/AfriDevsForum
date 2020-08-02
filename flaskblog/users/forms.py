from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from flaskblog.models import User


class RegistrationForm(FlaskForm): # for registraion form input 
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	country = SelectField('Select your country', validate_choice = True)
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')

	# for validating if username already exists in database
	def validate_username(self, username): 
		user = User.query.filter_by(username=username.data).first() #checks if username is in database
		if user:
			raise ValidationError('That username is taken. Please choose a different one')
	# for validating if email already exists in database
	def validate_email(self, email): 
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('That email is taken. Please choose a different one')


class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	country = SelectField('Country', validate_choice = True)
	picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])]) 
	submit = SubmitField('Update')

	# for validating if username already exists in database
	def validate_username(self, username): 
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first() #checks if username is in database
			if user:
				raise ValidationError('That username is taken. Please choose a different one')
	# for validating if email already exists in database
	def validate_email(self, email): 
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('That email is taken. Please choose a different one')

class RequestResetForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	submit = SubmitField('Request Password Reset')

	# for validating if email is for a registered user
	def validate_email(self, email): 
		user = User.query.filter_by(email=email.data).first()
		if user is None:
			raise ValidationError('There is no account with that email. You must first register.')

class ResetPasswordForm(FlaskForm):
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Reset Password')