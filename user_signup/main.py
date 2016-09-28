import webapp2
import jinja2
import os
import re

jinja_env = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)), 
	autoescape=True)

USER_RE = r"^[a-zA-Z0-9_-]{3,20}$"
PW_RE = r"^.{3,20}$"
EMAIL_RE = r"^[\S]+@[\S]+.[\S]+$"

USER_ERROR = "Invalid username"
PW_ERROR = "Invalid password"
VERIFY_ERROR = "Passwords don't match"
EMAIL_ERROR = "Invalid email address"


def build_validation_re(USER_RE, PW_RE, EMAIL_RE):
	return {'username': re.compile(USER_RE),
		'password': re.compile(PW_RE),
		'email': re.compile(EMAIL_RE)}


def build_error_messages(USER_ERROR, PW_ERROR, VERIFY_ERROR, EMAIL_ERROR):
	return {'username': USER_ERROR,
		'password': PW_ERROR,
		'verify': VERIFY_ERROR,
		'email': EMAIL_ERROR}


def validate(form_input, input_type):
	validation_re = build_validation_re(USER_RE, PW_RE, EMAIL_RE)
	validation_re = validation_re[input_type]
	return validation_re.match(form_input)


def validate_form(username, password, verify, email):
	username_valid = validate(username, 'username')
	password_valid = validate(password, 'password')
	verify_valid = password == verify
	
	if email:
		email_valid = validate(email, 'email')
	
	form_valid = True
	template_values = {'username': '',
		'email': '',
		'username_error': '',
		'password_error': '',
		'verify_error': '',
		'email_error': ''}

	error_messages = build_error_messages(USER_ERROR, PW_ERROR, VERIFY_ERROR, EMAIL_ERROR)

	form_valid = True
 	if not username_valid:
 		template_values['username_error'] = error_messages['username']
 		form_valid = False
 	else:
 		template_values['username'] = username
 	if not password_valid:
 		template_values['password_error'] = error_messages['password']
 		form_valid = False
 	if not verify_valid:
 		template_values['verify_error'] = error_messages['verify']
 		form_valid = False
 	if email and not email_valid:
 		template_values['email_error'] = error_messages['email']
 		form_valid = False
 	else:
 		template_values['email'] = email

	return form_valid, template_values


class SignupPage(webapp2.RequestHandler):
	def get(self):
		signup_form = jinja_env.get_template('/signup.html')
		self.response.write(signup_form.render())

	def post(self):
		form_valid, template_values = validate_form(
			username = self.request.get('username'),
			password = self.request.get('password'),
			verify = self.request.get('verify'),
			email = self.request.get('email'))

		if form_valid:
			username = self.request.get('username')
			self.redirect('/success?username=' + username)
		else:
			signup_form = jinja_env.get_template('/signup.html')
			self.response.write(signup_form.render(
				username=template_values['username'],
				email=template_values['email'],
				username_error=template_values['username_error'],
				password_error=template_values['password_error'],
				verify_error=template_values['verify_error'],
				email_error=template_values['email_error']))


class SuccessPage(webapp2.RequestHandler):
	def get(self):
		username = self.request.get('username')
		success = jinja_env.get_template('/success.html')
		self.response.write(success.render(username=username))


app = webapp2.WSGIApplication([
	('/signup', SignupPage),
	('/success', SuccessPage)
	], debug=True)

