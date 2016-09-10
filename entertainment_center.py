import media
import fresh_tomatoes
import requests
import json


def load_movie_input_data(infile):
	"""Load movie input data from JSON format into Python dict. Movie input 
	data contains IMDB ID and YouTube trailer URL."""
	with open(infile, 'r') as input_data:
		movie_input_data = json.load(input_data)
	return movie_input_data


def get_tmdb_info(imdb_id):
	"""Get poster image URL and short description from TMDB API
	https://www.themoviedb.org/documentation/api"""
	tmdb_lookup_url = "https://api.themoviedb.org/3/find/"
	tmdb_lookup_params = {'external_source':'imdb_id',
		'api_key':'c5aae1ee166b4cd8f830d077e3c1066f'}
	movie_req = requests.get(tmdb_lookup_url + imdb_id, params=tmdb_lookup_params)
	movie_response_dict = json.loads(movie_req.text).get('movie_results')[0]
	return movie_response_dict


def movie_flow():
	movies = []
	movie_input_data_file = 'movie_input_data.json'
	movie_input_data = load_movie_input_data(movie_input_data_file)
	for movie in movie_input_data['movies']:
		movie_response_dict = get_tmdb_info(movie['imdb_id'])
		title = movie_response_dict.get('title')
		description = movie_response_dict.get('overview')
		poster_url = 'https://image.tmdb.org/t/p/w600/' + movie_response_dict.get('poster_path')
		youtube_url = movie['youtube_url']
		movies.append(media.Movie(title, description, poster_url, youtube_url))
	fresh_tomatoes.open_movies_page(movies)


if __name__ == '__main__':
	movie_flow()

