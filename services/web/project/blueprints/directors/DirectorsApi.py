from flask_restful import Resource
from flask import request, redirect
from ...service import get_Directors, get_Director, create_director, update_director, delete_director


class DirectorsApi(Resource):
    def get(self):
        try:
            page = request.args['page']
        except:
            return redirect("/api/v1.0/directors?page=1")
        return get_Directors(page), 200

    def post(self):
        return create_director(**request.args), 200



class DirectorApi(Resource):
    def get(self, id):
        if id:
            return (get_Director(id))

    def put(self, id):
        return update_director(id, **request.args), 200

    def delete(self, id):
        return delete_director(id), 200