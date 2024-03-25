from flask_restful import Resource
from flask import request, redirect, current_app
from ...service import get_genres


class GenresApi(Resource):
    def get(self):
        current_app.logger.info("Getting genres")
        try:
            page = request.args['page']
        except:
            return redirect("/api/v1.0/genres?page=1")
        return {"genres": (get_genres())}, 200
