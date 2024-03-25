from flask import Blueprint
from flask_restful import Api
from .GenresApi import GenresApi

genres_api = Blueprint('genres', __name__, template_folder='/genres')
api = Api(genres_api)

api.add_resource(GenresApi, "/api/v1.0/genres")
