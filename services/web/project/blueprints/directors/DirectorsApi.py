from flask_restful import Resource
from flask import request, redirect, current_app
from ...service import get_directors, get_director, create_director, update_director, delete_director


class DirectorsApi(Resource):
    def get(self):
        current_app.logger.info("Getting directors")
        try:
            page = request.args['page']
        except:
            return redirect("/api/v1.0/directors?page=1")
        current_app.logger.info("Page: {}".format(page))
        return get_directors(page), 200

    def post(self):
        current_app.logger.info("Adding new director")
        current_app.logger.info("args: {}".format(request.args))
        return create_director(**request.args)



class DirectorApi(Resource):
    def get(self, id):
        current_app.logger.info("Getting director with id={}".format(id))
        return (get_director(id))

    def put(self, id):
        current_app.logger.info("Updating director with id={}".format(id))
        current_app.logger.info("args: {}".format(request.args))
        return update_director(id, **request.args)

    def delete(self, id):
        current_app.logger.info("Deleting director with id={}".format(id))
        return delete_director(id)