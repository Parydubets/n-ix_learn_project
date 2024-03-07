from flask_restful import Resource
from flask import request, redirect
from ...service import get_Films, get_Film


class FilmsApi(Resource):
    def get(self):
        result = dict(**request.args)
        result["films"] = get_Films(**request.args)
        return result, 200

    def post(self):
        return {"message": "Successfully added new film"}, 200


class FilmApi(Resource):
    def get(self, film_id):
        if film_id:
            return (get_Film(film_id))

        return {"message": "No id provided"}, 200

    def put(self, film_id):
        return {"message": "This endpoint updates a film with id={}".format(film_id)}, 200

    def delete(self, film_id):
        return {"message": "This endpoint deletes a film with id={}".format(film_id)}, 200
