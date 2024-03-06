from flask_restful import Resource
from flask import request
from ...service import get_Films


class FilmsApi(Resource):
    def get(self):
        parameters = request.args
        try:
            page = parameters['page']
        except:
            page = 1

        if len(parameters) > 0:
            return {"message": "This endpoint returns filtered/sorted films list"}, 200

        return {"message": print(get_Films(page).items)}, 200

    def post(self):
        return {"message": "Successfully added new film"}, 200


class FilmApi(Resource):
    def get(self, film_id):
        if film_id:
            return {"message": "This endpoint returns film with id={}".format(film_id)}, 200

        return {"message": "No id provided"}, 200

    def put(self, film_id):
        return {"message": "This endpoint updates a film with id={}".format(film_id)}, 200

    def delete(self, film_id):
        return {"message": "This endpoint deletes a film with id={}".format(film_id)}, 200
