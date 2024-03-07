""" The project init """
import os
from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from flask_restful import Resource, Api
from flask_migrate import Migrate
from dotenv import load_dotenv
from .models import db, User, Film, Director, Genre
from .blueprints.films import films_api
from .blueprints.directors import directors_api
from .blueprints.login import login_api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


def create_app(test_config=None):
    """
    The app creation func

    @param test_config:
    @type test_config:
    @return:
    @rtype:
    """
    # create and configure the app
    app = Flask(__name__)
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
        app.config.from_mapping(
            SECRET_KEY=os.getenv("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.getenv("SQLALCHEMY_DATABASE_URI")
        )
    else:
        app.config.from_mapping(
            SECRET_KEY=os.getenv("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.getenv("TEST_SQLALCHEMY_DATABASE_URI")
        )


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
            #result = Film.query.first()
            print(films_schema.dump(result))
            return 'SQLALCHEMY_DATABASE_URI:   '+str(os.getenv("SQLALCHEMY_DATABASE_URI")), 200


    app.register_blueprint(swagger_ui_blueprint, url_prefix=os.getenv("SWAGGER_URL"))
    app.register_blueprint(films_api)
    app.register_blueprint(directors_api)
    app.register_blueprint(login_api)
    api.add_resource(HelloWorld, "/")


    return app
