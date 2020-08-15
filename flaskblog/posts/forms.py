from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
	title = StringField('Title', validators = [DataRequired()])
	content = CKEditorField('Content', validators = [DataRequired()])
	tag = StringField('Tags', validators = [DataRequired()])
	submit = SubmitField('Post')
