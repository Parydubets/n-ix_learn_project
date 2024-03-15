from flask_restful import Resource
from flask import request, current_app, send_from_directory, jsonify
from ...service import check_film_fileds, get_films, get_film_img, add_film, update_film, get_film, delete_film
from werkzeug.utils import secure_filename
import os

class FilmsApi(Resource):
    def get(self):
        result = get_films(**request.args)
        return result, 200

    def post(self):
        film_dict={**request.args}
        try:
            file = request.files['poster']
            filename = secure_filename(file.filename)
            film_dict["poster"]=filename
        except:
            return {"error": "no poster file attached"}
        if len(film_dict)<7 or 6>len(film_dict)>8:
            return {"error": "not all necessary parameters provided"}
        error = check_film_fileds(**film_dict)
        if len(error)>0:
            return {"error: ": error}
        else:
            file.save(os.path.join("project/static/", filename))
            return {"added film":add_film(**film_dict)}


class FilmApi(Resource):
    def get(self, id):
        if id:
            return (get_film(id))
        return {"message": "No id provided"}, 200

    def put(self, id):
        film_dict={**request.args}
        try:
            file = request.files['poster']
            filename = secure_filename(file.filename)
            film_dict["poster"] = filename
        except:
            pass
        error = check_film_fileds(**film_dict)

        if len(error) > 0:
            return {"errors: ": error}
        else:
            #file.save(os.path.join("project/static/", filename))
            return {"updated film": update_film(id, **film_dict)}
        return {"message": "This endpoint updates a film with id={}".format(id)}, 200

    def delete(self, id):
        return delete_film(id), 200


class FilmApiPoster(Resource):
    def get(self, id):
        image_name = get_film_img(id)
        if image_name is None:
            return {"error": "no poster file"}
        try:
            return send_from_directory(directory="static", path=image_name, as_attachment=True)
        except FileNotFoundError:
            return 404
