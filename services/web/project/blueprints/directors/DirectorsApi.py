from flask_restful import Resource
from flask import request, redirect
from ...service import get_Directors, get_Director


class DirectorsApi(Resource):
    def get(self):
        try:
            page = request.args['page']
        except:
            return redirect("/api/v1.0/directors?page=1")
        return {"page": page,
                "films": (get_Directors(page))}, \
            200

    def post(self):
        return {"message": "This endpoint adds a new director"}, 200

    def put(self):
        return {"message": "This endpoint updates a director"}, 200

    def delete(self):
        return {"message": "This endpoint deletes a director"}, 200


class DirectorApi(Resource):
    def get(self, id):
        if id:
            return (get_Director(id))

        return {"message": "No id provided"}, 200
    def put(self, director_id):
        return {"message": "This endpoint updates a director with id={}".format(director_id)}, 200

    def delete(self, director_id):
        return {"message": "This endpoint deletes a director with id={}".format(director_id)}, 200