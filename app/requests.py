from .models import Quote
import requests
 


#getting the movie base url
base_url = None

def configure_request(app):
    global base_url
    base_url = app.config['QUOTE_API_BASE_URL']


def get_quotes():
    '''
    Function that gets the json response to our url request
    '''
    get_quote_response = requests.get('http://quotes.stormconsultancy.co.uk/random.json').json()
    print(get_quote_response)
    return get_quote_response

# def process_results(movie_list):
#     '''
#     Function that processes the movie result and transform them to a list of objects

#     Args:
#         movie_list: A list of dictionaries that contain movie details

#     Returns:
#         movie_results: A list of movie objects
#     '''

#     quote_results = []

#     for quote_item in movie_list:
#         id = movie_item.get('id')
#         title = movie_item.get('original_title')
#         overview = movie_item.get('overview')
#         poster = movie_item.get('poster_path')
#         vote_average = movie_item.get('vote_average')
#         vote_count = movie_item.get('vote_count')

#         if poster:
#             movie_object = Movie(id,title,overview,poster,vote_average,vote_count)
#             movie_results.append(movie_object)
            
#     return movie_results
