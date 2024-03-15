from flask import Blueprint
from flask_restful import Api
from .FilmsApi import FilmsApi, FilmApi, FilmApiPoster

films_api = Blueprint('films', __name__, template_folder='/films')
api = Api(films_api)

api.add_resource(FilmsApi, "/api/v1.0/films")
api.add_resource(FilmApi, "/api/v1.0/films/<int:id>")
api.add_resource(FilmApiPoster, "/api/v1.0/films/<int:id>/poster")