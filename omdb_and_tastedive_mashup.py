'''
This project will take you through the process of mashing up data from two different APIs to make movie recommendations.
The TasteDive API lets you provide a movie (or bands, TV shows, etc.) as a query input, and returns a set of related
items. The OMDB API lets you provide a movie title as a query input and get back data about the movie, including scores
from various review sites (Rotten Tomatoes, IMDB, etc.).

You will put those two together. You will use TasteDive to get related movies for a whole list of titles.
You’ll combine the resulting lists of related movies, and sort them according to their Rotten Tomatoes scores
(which will require making API calls to the OMDB API.)

To avoid problems with rate limits and site accessibility, we have provided a cache file with results for all the
queries you need to make to both OMDB and TasteDive. Just use requests_with_caching.get() rather than requests.get().
If you’re having trouble, you may not be formatting your queries properly, or you may not be asking for data that exists
in our cache. We will try to provide as much information as we can to help guide you to form queries for which data
exists in the cache.

Your first task will be to fetch data from TasteDive. The documentation for the API is at https://tastedive.com/read/api.

Define a function, called get_movies_from_tastedive. It should take one input parameter, a string that is the name of
a movie or music artist. The function should return the 5 TasteDive results that are associated with that string;
be sure to only get movies, not other kinds of media. It will be a python dictionary with just one key, ‘Similar’.

Try invoking your function with the input “Black Panther”.

HINT: Be sure to include only q, type, and limit as parameters in order to extract data from the cache.
If any other parameters are included, then the function will not be able to recognize the data that you’re attempting
to pull from the cache. Remember, you will not need an api key in order to complete the project, because all data will
be found in the cache.
'''
import requests_with_caching   # module available only in Runestone environment

def get_movies_from_tastedive(name):
    baseurl = 'https://tastedive.com/api/similar'
    params_dict = {}
    params_dict['q'] = name
    params_dict['type'] = 'movies'
    params_dict['limit'] = 5
    resp = requests_with_caching.get(baseurl, params=params_dict)
    return resp.json()


def extract_movie_titles(movies_dict):
    moviesLst = []
    movies = movies_dict['Similar']['Results']
    for movie in movies:
        moviesLst.append(movie['Name'])
    return moviesLst


def get_related_titles(movie_titles_lst):
    related_movies_lst = []
    for movie_title in movie_titles_lst:
        movies_dict = get_movies_from_tastedive(movie_title)
        moviesLst = extract_movie_titles(movies_dict)
        for movie in moviesLst:
            if movie not in related_movies_lst:
                related_movies_lst.append(movie)
    return related_movies_lst


def get_movie_data(movie_title):
    baseurl = 'http://www.omdbapi.com/'
    params_dict = {}
    params_dict['t'] = movie_title
    params_dict['r'] = 'json'
    resp = requests_with_caching.get(baseurl, params=params_dict)
    return resp.json()


def get_movie_rating(omdb_dict):
    ratings = omdb_dict['Ratings']
    for rating in ratings:
        if rating['Source'] == 'Rotten Tomatoes':
            return int(rating['Value'][:-1])
    return 0


def get_sorted_recommendations(movie_titles_lst):
    related_movie_lst = get_related_titles(movie_titles_lst)
    movie_lst = []
    sorted_lst = []
    for movie in related_movie_lst:
        rating = get_movie_rating(get_movie_data(movie))
        movie_lst.append((rating, movie))
    movie_lst = sorted(movie_lst, reverse=True)
    for rating, title in movie_lst:
        sorted_lst.append(title)
    return sorted_lst

# some invocations that we use in the automated tests; uncomment these if you are getting errors and want better error messages
print(get_sorted_recommendations(["Bridesmaids", "Sherlock Holmes"]))
