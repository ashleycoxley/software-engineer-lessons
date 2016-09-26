import webapp2
import jinja2
import os
import re

jinja_env = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)), 
	autoescape=True)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PW_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")

def validate_username(username):
	return USER_RE.match(username)

def validate_password(password):
	return PW_RE.match(password)

def validate_email(email):
	return EMAIL_RE.match(email)


class SignupPage(webapp2.RequestHandler):
	def get(self):
		signup_form = jinja_env.get_template('/signup.html')
		self.response.write(signup_form.render())

	def post(self):
		username_error = ""
		password_error = ""
		verify_error = ""
		email_error = ""

		username = self.request.get('username')
		password = self.request.get('password')
		verify = self.request.get('verify')
		email = self.request.get('email')

		username_valid = validate_username(username)
		password_valid = validate_password(password)
		verify_valid = password == verify
		if email:
			email_valid = validate_email(email)

		form_valid = True
		if not username_valid:
			username_error = "Invalid username"
			username = ""
			form_valid = False
		if not password_valid:
			password_error = "Invalid password"
			form_valid = False
		if not verify_valid:
			verify_error = "Passwords don't match"
			form_valid = False
		if email and not email_valid:
			email_error = "Invalid email"
			email = ""
			form_valid = False

		if form_valid:
			self.redirect('/success?username=' + username)
		else:
			signup_form = jinja_env.get_template('/signup.html')
			self.response.write(signup_form.render(
				username=username,
				email=email,
				username_error=username_error,
				password_error=password_error,
				verify_error=verify_error,
				email_error=email_error))


class SuccessPage(webapp2.RequestHandler):
	def get(self):
		username = self.request.get('username')
		success = jinja_env.get_template('/success.html')
		self.response.write(success.render(username=username))


app = webapp2.WSGIApplication([
	('/signup', SignupPage),
	('/success', SuccessPage)
	], debug=True)

