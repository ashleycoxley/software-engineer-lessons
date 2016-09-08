import media
import fresh_tomatoes

upstream_color = media.Movie("Upstream Color",
	"""A man and woman are drawn together, entangled in the life cycle of an 
	ageless organism. Identity becomes an illusion as they struggle to assemble
	the loose fragments of wrecked lives.""",
	"https://upload.wikimedia.org/wikipedia/en/e/ea/Upstream_Color_poster.jpg",
	"https://www.youtube.com/watch?v=5U9KmAlrEXU")

fargo = media.Movie("Fargo",
	"""Jerry Lundegaard's inept crime falls apart due to his and his henchmen's
	bungling and the persistent police work of the quite pregnant Marge Gunderson.""",
	"http://vignette3.wikia.nocookie.net/fargo/images/d/d7/Fargo_movieposter.jpg/revision/latest?cb=20140226224031",
	"https://www.youtube.com/watch?v=h2tY82z3xXU")



if __name__ == '__main__':
	movies = [upstream_color, fargo]
	fresh_tomatoes.open_movies_page(movies)