from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.fields import StringField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import TextInput


class TagListField(StringField):
    widget = TextInput()
    """StringField for a list of separated tags"""

    def __init__(self, label = 'Tags', validators = None, remove_duplicates = True, to_lowercase = True, separator = '',
                 **kwargs):
        """
        Construct a new field.
        :param label: The label of the field.
        :param validators: A sequence of validators to call when validate is called.
        :param remove_duplicates: Remove duplicates in a case insensitive manner.
        :param to_lowercase: Cast all values to lowercase.
        :param separator: The separator that splits the individual tags.
        """
        super(TagListField, self).__init__(label, validators, **kwargs)
        self.remove_duplicates = remove_duplicates
        self.to_lowercase = to_lowercase
        self.separator = separator
        self.data = []

    def _value(self):
        if self.data:
            return u', '.join(self.data)
        else:
            return u''

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = [x.strip() for x in valuelist[0].split(self.separator)]
            if self.remove_duplicates:
                self.data = list(self._remove_duplicates(self.data))
            if self.to_lowercase:
                self.data = [x.lower() for x in self.data]

    @classmethod
    def _remove_duplicates(cls, seq):
        """Remove duplicates in a case insensitive, but case preserving manner"""
        d = {}
        for item in seq:
            if item.lower() not in d:
                d[item.lower()] = True
                yield item


class PostForm(FlaskForm):
    title = StringField('Title', validators = [DataRequired()])
    content = CKEditorField('Content', validators = [DataRequired()])
    tags = TagListField('Tags', separator = ',',
                        validators = [Length(max = 8, message = "You can only use up to 8 tags.")])
    submit = SubmitField('Post')


class CommentForm(FlaskForm):
    body = StringField('Enter your comment', validators = [DataRequired()])
    submit = SubmitField('Comment')


class SearchForm(FlaskForm):
    search = StringField('Search', validators = [DataRequired()])
    submit = SubmitField('Search')
