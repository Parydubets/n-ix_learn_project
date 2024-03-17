from flask_restful import Resource
from flask import request, redirect
from ...service import get_genres


class GenresApi(Resource):
    def get(self):
        try:
            page = request.args['page']
        except:
            return redirect("/api/v1.0/genres?page=1")
        return {"genres": (get_genres())}, \
            200

    def post(self):
        return {"message": "This endpoint adds a new director"}, 200
