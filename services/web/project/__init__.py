""" The project init """
import os
import csv
import subprocess
from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from flask_restful import Resource, Api
from flask_migrate import Migrate
from dotenv import load_dotenv
from .models import db, User, Film, Director, Genre
from .blueprints.films import films_api
from .blueprints.directors import directors_api
from .blueprints.login import login_api


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
    load_dotenv()
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


    migrate = Migrate(app, db, 'web/migrations')

    db.init_app(app)

    class HelloWorld(Resource):
        def get(self):
            """
            @return: Hello world, <SQLALCHEMY_DATABASE_URI>
            @rtype: String
            """
            return 'SQLALCHEMY_DATABASE_URI:   '+str(os.getenv("SQLALCHEMY_DATABASE_URI")), 200


    class Seed(Resource):
        def get(self):
            """
            @return: Hello, world!
            @rtype: String
            """
            subprocess.run(["flask", "db", "upgrade"])
            subprocess.run(["flask", "db", "migrate"])
            subprocess.run(["flask", "db", "upgrade"])
            subprocess.run(["flask", "seed"])
            return {"message": "Hello, World!"}, 200


    app.register_blueprint(swagger_ui_blueprint, url_prefix=os.getenv("SWAGGER_URL"))
    app.register_blueprint(films_api)
    app.register_blueprint(directors_api)
    app.register_blueprint(login_api)
    api.add_resource(HelloWorld, "/")
    api.add_resource(Seed, "/api/seed")


    def seed_from_file_decorator(function):
        def wrapper(*args, **kwargs):
            result = function(*args, **kwargs)
            with open(result[0], "r") as f:
                file = f.read()
            data = list(csv.reader(file, delimiter=","))
            is_created = result[2].query.first()
            if not is_created:
                for item in data:
                    if result[2] is Film:
                        genres = item[-1].split('_')
                        item = item[0:-1]
                        values = dict(zip(result[1], item))
                        object_in = result[2](**values)

                        for i in genres:
                            genre = Genre.query.where(Genre.name == i).first()
                            if genre is not None:
                                object_in.genres.append(genre)
                    else:
                        values = dict(zip(result[1], item))
                        object_in = result[2](**values)
                    if 'is_admin' in result[1]:
                        object_in.is_admin = bool(values['is_admin'])

                    db.session.add(object_in)
                    db.session.commit()
            return result
        return wrapper


    @seed_from_file_decorator
    def seed_from_file(file, table):
        if table == 'Users':
            return file, User.__table__.columns.keys(), User
        if table == 'Directors':
            return file, Director.__table__.columns.keys(), Director
        if table == 'Genres':
            return file, Genre.__table__.columns.keys(), Genre
        if table == 'Films':
            return file, Film.__table__.columns.keys(), Film



    @app.cli.command('seed')
    def seed():
        with app.app_context():
            subprocess.run(["flask", "db", "init"])
            subprocess.run(["flask", "db", "upgrade"])
            subprocess.run(["flask", "db", "migrate"])
            subprocess.run(["flask", "db", "upgrade"])
            seed_from_file("./project/static/seed/directors_mock.csv", 'Directors')
            seed_from_file("./project/static/seed/users_mock.csv", 'Users')
            seed_from_file("./project/static/seed/genres_mock.csv", 'Genres')
            seed_from_file("./project/static/seed/films_mock.csv", 'Films')

    return app
