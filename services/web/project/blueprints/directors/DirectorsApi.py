from flask_restful import Resource
from flask import request


class DirectorsApi(Resource):
    def get(self):
        if request.args.get("id"):
            return {"message": "This endpoint returns director with"
                               " id={}".format(request.args.get("id"))}, 200

        return {"message": "This endpoint returns directors list"}, 200

    def post(self):
        return {"message": "This endpoint adds a new director"}, 200

    def put(self):
        return {"message": "This endpoint updates a director"}, 200

    def delete(self):
        return {"message": "This endpoint deletes a director"}, 200


class DirectorApi(Resource):
    def get(self, director_id):
        if director_id:
            return {"message": "This endpoint returns director with id={}".format(director_id)}, 200

        return {"message": "No id provided"}, 200
    def put(self, director_id):
        return {"message": "This endpoint updates a director with id={}".format(director_id)}, 200

    def delete(self, director_id):
        return {"message": "This endpoint deletes a director with id={}".format(director_id)}, 200