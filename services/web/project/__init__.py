""" The project init """
import os
from flask import Flask, send_from_directory, request
from werkzeug.utils import secure_filename
from flask_swagger_ui import get_swaggerui_blueprint
from flask_restful import Resource, Api
from flask_migrate import Migrate
from dotenv import load_dotenv
from .models import db, User, Film, Director, Genre
from .blueprints.films import films_api
from .blueprints.directors import directors_api
from .blueprints.login import login_api
from .blueprints.genres import genres_api
from flask_marshmallow import Marshmallow
from .config import Config, Config_Test


def create_app(test_config=None):
    """
    The app creation func

    @param test_config:
    @type test_config:
    @return:
    @rtype:
    """
    # create and configure the app
    app = Flask(__name__, static_folder='static')
    api = Api(app)

    load_dotenv("../../.env.dev")
    swagger_ui_blueprint = get_swaggerui_blueprint(
        os.getenv("SWAGGER_URL"),
        os.getenv("API_URL"),
        config={
            'app_name': 'Access API'
        }
    )

    if test_config is None:
        app.config.from_object(Config)
    else:
        app.config.from_object(Config_Test)

    migrate = Migrate(app, db, 'project/migrations')

    db.init_app(app)
    ma = Marshmallow()
    ma.init_app(app)

    class HelloWorld(Resource):
        def get(self):
            """
            @return: Hello world, <SQLALCHEMY_DATABASE_URI>
            @rtype: String
            """

            class FilmSchema(ma.SQLAlchemyAutoSchema):
                class Meta:
                    model = Film
                    include_fk = True

            film_schema = FilmSchema()
            films_schema = FilmSchema(many=True)
            result = Film.query.paginate(page=int(1), per_page=10)
            return 'SQLALCHEMY_DATABASE_URI:   '+str(os.getenv("SQLALCHEMY_DATABASE_URI")), 200


    app.register_blueprint(swagger_ui_blueprint, url_prefix=os.getenv("SWAGGER_URL"))
    app.register_blueprint(films_api)
    app.register_blueprint(directors_api)
    app.register_blueprint(login_api)
    app.register_blueprint(genres_api)
    api.add_resource(HelloWorld, "/")

    # Get Image file Routing
    @app.route("/get-image/<path:image_name>", methods=['GET', 'POST'])
    def get_image(image_name):

        try:
            return send_from_directory(directory="static", path=image_name, as_attachment=True), 200

        except FileNotFoundError:
           return 404

    @app.route("/upload", methods=["GET", "POST"])
    def upload_file():
        if request.method == "POST":
            file = request.files["file"]
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["MEDIA_FOLDER"], filename))
        return """
        <!doctype html>
        <title>upload new File</title>
        <form action="" method=post enctype=multipart/form-data>
          <p><input type=file name=file><input type=submit value=Upload>
        </form>
        """

    return app
