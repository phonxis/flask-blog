from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired

class LoginForm(Form):
	username = StringField('usernamename', validators=[DataRequired()])
	password = StringField('password', validators=[DataRequired()])
	remember_me = BooleanField('remember_me', default=False)

class PostForm(Form):
	post = TextAreaField('post', validators=[DataRequired()])
	title = TextAreaField('title', validators=[DataRequired()])
