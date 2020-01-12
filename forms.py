from wtforms import *
from wtforms.validators import *
from models import *

def login_free(form, field):
	login = field.data
	check = User.get(login=login)
	if check is not None:
		raise ValidationError('Login %r is already taken' % login)

def email_free(form, field):
	email = field.data
	check = User.get(email=email)
	if check is not None:
		raise ValidationError('E-mail %r is already in use' % email)

def len_check(form, field):
	pwd = field.data
	if len(pwd) < 5:
		raise ValidationError('Your password is too short, use 5 or more characters')

def pwd_check(form, field):
	pwd2 = field.data
	pwd1 = form.pwd1.data
	if pwd1 != pwd2:
		raise ValidationError('Passwords should match')

def secret_key_check(form, field):
	secret_key = '5656'
	key = form.secret_key.data
	if key != secret_key:
		raise ValidationError('Wrong secret key')

def login_check(form, field):
	login = field.data
	check = User.get(login=login)
	if check is None:
		raise ValidationError('User with login %r not found' % login)

def pwd_match_check(form, field):
	login = form.login.data
	pwd = field.data
	check = User.get(login=login, pwd=pwd)
	if check is None:
		raise ValidationError('Wrong password. Try again')

def com_title_free(form, field):
	title = field.data
	check = User.get(login=title)
	if check is not None:
		raise ValidationError('Title is already in use')

def com_email_free(form, field):
	email = field.data
	check = User.get(email=email)
	if check is not None:
		raise ValidationError('E-mail is already in use')

def com_title_check(form, field):
	title = field.data
	check = User.get(login=title)
	if check is None:
		raise ValidationError('Title %r was not found' % title)

def com_pwd_check(form, field):
	pwd = field.data
	com = User.get(login=form.title.data)
	if com.pwd != pwd:
		raise ValidationError('Password do not match. Try again')

def positive_integer_check(form, field):
	value = field.data
	try:
		v = int(value)
	except Exception:
		raise ValidationError('integer required')

	if v < 0:
		raise ValidationError('positive number required')

class RegForm(Form):
	login = StringField('Login', [InputRequired(), login_free])
	email = StringField('E-mail', [InputRequired(), email_free])
	pwd1 = PasswordField('Password', [InputRequired(), len_check])
	pwd2 = PasswordField('Password again', [InputRequired(), pwd_check])


class LoginForm(Form):
	login = StringField('Login', [InputRequired(), login_check])
	pwd = PasswordField('Password', [InputRequired(), pwd_match_check])


class comRegForm(Form):
	title = StringField('Title', [InputRequired(), com_title_free])
	email = StringField('E-mail', [InputRequired(), com_email_free])
	pwd1 = PasswordField('Password', [InputRequired(), len_check])
	pwd2 = PasswordField('Password again', [InputRequired(), pwd_check])
	secret_key = PasswordField('Wrong secret key', [InputRequired(), secret_key_check])


class comLoginForm(Form):
	title = StringField('Title', [InputRequired(), com_title_check])
	pwd = PasswordField('Password', [InputRequired(), com_pwd_check])


class comNewDishForm(Form):
	title = StringField('Title', [InputRequired()])
	description = StringField('Description', [InputRequired()])
	type_of_food = StringField('Type_of_food', [InputRequired()])
	price = IntegerField('Price', [InputRequired(), positive_integer_check])
	small = StringField('Small', [InputRequired()])
	cover = StringField('Small', [InputRequired()])

