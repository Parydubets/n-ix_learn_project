from flask_restful import Resource
from flask_login import login_required
from flask import request, send_from_directory, current_app
from ...service import check_film_fileds, get_films, get_film_img, add_film,\
                        update_film, get_film, delete_film
from werkzeug.utils import secure_filename
import os
from ...models import users

class FilmsApi(Resource):

    def get(self):
        current_app.logger.info("Requesting films")
        return get_films(**request.args)


    @login_required
    def post(self):
        current_app.logger.info("Adding new film")
        film_dict={**request.args}
        try:
            file = request.files['poster']
            filename = secure_filename(file.filename)
            film_dict["poster"]=filename
            current_app.logger.info("Trying to get poster file")
        except:
            current_app.logger.warning("No poster file")
            return {"error": "no poster file attached"}, 400
        else:
            current_app.logger.info("args: {}".format(request.args))
            file.save(os.path.join("project/static/", filename))
            return add_film(**film_dict)


class FilmApi(Resource):
    def get(self, id):
        current_app.logger.info("Getting film with id={}".format(id))
        return (get_film(id))


    @login_required
    def put(self, id):
        current_app.logger.info("Updating film with id={}".format(id))
        film_dict={**request.args}
        try:
            file = request.files['poster']
            filename = secure_filename(file.filename)
            film_dict["poster"] = filename
        except:
            pass
        error = check_film_fileds(**film_dict)
        current_app.logger.info("args: {}".format(request.args))
        if len(error) > 0:
            current_app.logger.warning("errors: {}".format(error))
            return {"errors: ": error}, 400
        else:
            return update_film(id, **film_dict)

    @login_required
    def delete(self, id):
        current_app.logger.info("Deleting film with id={}".format(id))
        deletion = delete_film(id)
        if 'error' in deletion:
            return deletion, 400
        return deletion, 200


class FilmApiPoster(Resource):
    def get(self, id):
        current_app.logger.info("Getting poster for film with id={}".format(id))
        image_name = get_film_img(id)
        if "error" in image_name:
            return image_name, 400
        try:
            return send_from_directory(directory="static", path=image_name, as_attachment=True)
        except FileNotFoundError:
            current_app.logger.warning("Poster file not dound")
            return {"error": "Poster file not found"}
