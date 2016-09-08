
class Movie():
	"""
	Representation of an individual movie.

	Attributes:
		title (str): Movie title
		storyline (str): Simple movie plot description
		poster_image (str): URL for movie poster poster image 
		youtube_trailer (str): URL for YouTube movie trailer

	"""
	def __init__(self, title, storyline, poster_image, youtube_trailer):
		self.title = title
		self.storyline = storyline
		self.poster_image_url = poster_image
		self.trailer_youtube_url = youtube_trailer