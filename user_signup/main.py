import webapp2
import jinja2
import os
import re
import random
import string
import hashlib
import hmac

from google.appengine.ext import ndb


jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)), 
    autoescape=True)

USER_RE = r"^[a-zA-Z0-9_-]{3,20}$"
PW_RE = r"^.{3,20}$"
EMAIL_RE = r"^[\S]+@[\S]+.[\S]+$"

USER_ERROR = "Invalid username"
USER_EXISTS_ERROR = "User already exists"
PW_ERROR = "Invalid password"
VERIFY_ERROR = "Passwords don't match"
EMAIL_ERROR = "Invalid email address"

SECRET = 'maple'

VALIDATION_RE = {'username': re.compile(USER_RE),
        'password': re.compile(PW_RE),
        'email': re.compile(EMAIL_RE)}

ERROR_MESSAGES = {'username': USER_ERROR,
        'user_exists': USER_EXISTS_ERROR,
        'password': PW_ERROR,
        'verify': VERIFY_ERROR,
        'email': EMAIL_ERROR}


def validate(form_input, input_type):
    validation = VALIDATION_RE[input_type]
    return validation.match(form_input)


def validate_form(username, password, verify, email):
    user_query = User.query(User.username==username)
    user_exists = user_query.get()

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

    form_valid = True
    if not username_valid:
        template_values['username_error'] = ERROR_MESSAGES['username']
        form_valid = False
    else:
        if user_exists:
            template_values['username_error'] = ERROR_MESSAGES['user_exists']
            form_valid = False
        else:
            template_values['username'] = username
    if not password_valid:
        template_values['password_error'] = ERROR_MESSAGES['password']
        form_valid = False
    if not verify_valid:
        template_values['verify_error'] = ERROR_MESSAGES['verify']
        form_valid = False
    if email and not email_valid:
        template_values['email_error'] = ERROR_MESSAGES['email']
        form_valid = False
    else:
        template_values['email'] = email

    return form_valid, template_values


def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(5))


def hash_password(username, password, salt=None):
    if salt == None:
        salt = make_salt()
    h = hashlib.sha256(username + password + salt).hexdigest()
    return '%s,%s' % (h, salt)


def validate_password(username, password, h):
    salt = h.split(',')[1]
    if make_pw_hash(name, pw, salt) == h:
        return True
    else:
        return False


def hash_cookie(user_id):
    user_hash = hmac.new(SECRET, user_id).hexdigest()
    return "%s|%s" % (user_id, user_hash)


def build_cookie_str(user_id):
    cookie_hash = hash_cookie(user_id)
    return 'user_id=%s; Path=/' % cookie_hash


def validate_cookie(cookie_hash):
    returned_user_id = cookie_hash.split('|')[0]
    if cookie_hash == hash_cookie(returned_user_id):
        return returned_user_id


class User(ndb.Model):
    username = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)
    email = ndb.StringProperty()
    time_added = ndb.DateTimeProperty(auto_now_add=True)


class SignupPage(webapp2.RequestHandler):
    def get(self):
        signup_form = jinja_env.get_template('/signup.html')
        self.response.write(signup_form.render())

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        form_valid, template_values = validate_form(username, password, verify, email)

        if form_valid:
            password_hash = hash_password(username, password)
            user = User(username=username, password=password_hash)
            if email:
                user.email = email
            user_key = user.put()
            user_id = str(user_key.id())
            cookie_str = build_cookie_str(user_id)

            self.response.headers.add_header('Set-Cookie', cookie_str)
            self.redirect('/success')
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
        cookie_hash = self.request.cookies.get('user_id')
        returned_user_id = validate_cookie(cookie_hash)
        if returned_user_id:
            user_entity = User.get_by_id(int(returned_user_id))
            username = user_entity.username
            success = jinja_env.get_template('/success.html')
            self.response.write(success.render(username=username))
        else:
            self.redirect('/signup')


class BasePage(webapp2.RequestHandler): # placeholder for blog content
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Main page')


app = webapp2.WSGIApplication([
    ('/', BasePage),
    ('/signup', SignupPage),
    ('/success', SuccessPage)
    ], debug=True)

