from flask import Blueprint
from flask_restful import Api
from .DirectorsApi import DirectorsApi, DirectorApi

directors_api = Blueprint('directors', __name__, template_folder='/directors')
api = Api(directors_api)

api.add_resource(DirectorsApi, "/api/v1.0/directors")
api.add_resource(DirectorApi, "/api/v1.0/directors/<int:id>")
