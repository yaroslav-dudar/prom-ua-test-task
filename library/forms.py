from wtforms import Form, PasswordField, TextField, validators
from wtforms.validators import ValidationError

from database import db_session
from models import User

class AuthForm(Form):	
	email = TextField('Email', [validators.Length(min=6, max=120), validators.Email()])
	password =  PasswordField('Password', [validators.Length(min=6, max=25)])

	def validate_all(self, field):
		user = db_session.query(User).filter(
			User.password == self.password.data, User.email == self.email.data).first()
		if not user:
			raise ValidationError('Please enter a correct username and password')


class RegistrationForm(Form):
	first_name = TextField('First name', [validators.Length(min=2, max=50)])
	last_name = TextField('Last name', [validators.Length(min=2, max=50)])
	email = TextField('Email', [validators.Length(min=6, max=120), validators.Email()])
	password = PasswordField('Password', [validators.Required(),
		validators.EqualTo('confirm', message='Passwords must match'),validators.Length(min=6, max=16)])
	confirm = PasswordField('Repeat Password')