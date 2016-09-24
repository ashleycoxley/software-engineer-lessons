
import os
import webapp2
import jinja2


jinja_env = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)), 
	autoescape=True)


def encode_algo(character):
	# save case of character, convert to lower if upper
	lower_case = True
	if character.isupper():
		lower_case = False
		character = character.lower()

	alphabet = 'abcdefghijklmnopqrstuvwxyz'
	idx = alphabet.index(character)
	if idx <= 12:
		code_idx = idx + 13
	else:
		code_idx = idx - 13
	encoded_char = alphabet[code_idx]

	return(encoded_char, lower_case)


def rot13_encode(input_str):
	output_str = ''
	if input_str:
		for char in input_str:
			if char.isalpha():
				encoded_char, lower_case = encode_algo(char)
				if not lower_case:
					encoded_char = encoded_char.upper()
				output_str += encoded_char
			else:
				output_str += char

	return output_str


class MainPage(webapp2.RequestHandler):
	def get(self):
		print "hey"
		form = jinja_env.get_template("form.html")
		self.response.write(form.render())

	def post(self):
		text = self.request.get('text')
		encoded_text = rot13_encode(text)
		form = jinja_env.get_template("form.html")
		self.response.write(form.render(text=encoded_text))


app = webapp2.WSGIApplication([
	('/', MainPage)], debug=True)
