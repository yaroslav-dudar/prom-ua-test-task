from wtforms import (Form, PasswordField, TextField,
	validators, HiddenField, SelectMultipleField)
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from wtforms.validators import ValidationError

from database import db_session
from models import User, Writer, Book

class AuthForm(Form):	
	email = TextField('Email', [validators.Length(min=6, max=120), validators.Email()])
	password =  PasswordField('Password', [validators.Length(min=6, max=25)])

	def validate_email(self, field):
		user = db_session.query(User).filter(
			User.password == self.password.data, User.email == self.email.data).first()
		if not user:
			raise ValidationError('Please enter a correct username and password')


class RegistrationForm(Form):
	first_name = TextField('First name', [validators.Length(min=2, max=50), validators.Required()])
	last_name = TextField('Last name', [validators.Length(min=2, max=50), validators.Required()])
	email = TextField('Email', [validators.Length(min=6, max=120), validators.Email(), validators.Required()])
	password = PasswordField('Password', [validators.Required(),
		validators.EqualTo('confirm', message='Passwords must match'),validators.Length(min=6, max=16)])
	confirm = PasswordField('Repeat Password')


class WriterEditForm(Form):
	id = HiddenField('id')
	name = TextField('Name', [validators.Length(min=2, max=50)])

	def validate_name(self, field):
		writer = Writer.query.filter(Writer.name == field.data,
			Writer.id != self.id.data).first()
		if writer:
			raise ValidationError('Existing writer with the same name.')


class WriterAddForm(Form):
	name = TextField('Name', [validators.Length(min=2, max=50)])

	def validate_name(self, field):
		writer = db_session.query(Writer).filter(Writer.name == field.data).first()
		if writer:
			raise ValidationError('Existing writer with the same name.')


class BookAddForm(Form):
	title = TextField('Title', [validators.Length(min=2, max=100)])
	writers = QuerySelectMultipleField('Writers', query_factory=Writer.query.all)

	def validate_title(self, field):
		book = Book.query.filter_by(title=field.data).first()
		if book:
			raise ValidationError('Existing book with the same title.')

	def validate_writers(self, field):
		if len(field.data) == 0:
			raise ValidationError('Please add writer(s) for current book.')


class BookEditForm(Form):
	id = HiddenField('id')
	title = TextField('Title', [validators.Length(min=2, max=100)])
	writers = SelectMultipleField('Writers', choices=[], coerce=int)

	def __init__(self, *args, **kwargs):
		super(BookEditForm, self).__init__(*args, **kwargs)
		self.writers.choices =	[(writer.id, writer) for writer in Writer.query.all()]
		self.validate() 

	def validate_title(self, field):
		book = Book.query.filter(
			Book.title == self.title.data, Book.id != self.id.data).first()
		if book:
			raise ValidationError('Existing book with the same title.')

	def validate_writers(self, field):
		if not field.data:
			raise ValidationError('Please add writer(s) for current book.')