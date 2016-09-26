import os
import webapp2
import jinja2


jinja_env = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)), 
	autoescape=True)


class MainPage(webapp2.RequestHandler):
	def get(self):
		form = jinja_env.get_template("form.html")
		self.response.write(form.render())

	def post(self):
		text = self.request.get('text')
		encoded_text = text.encode('rot13')
		form = jinja_env.get_template("form.html")
		self.response.write(form.render(text=encoded_text))


app = webapp2.WSGIApplication(('/', MainPage), debug=True)