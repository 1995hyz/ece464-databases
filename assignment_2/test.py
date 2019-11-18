from pymongo import MongoClient


def query_movie(movie_name, collection):
    movie = collection.find({"title": movie_name})
    return movie
