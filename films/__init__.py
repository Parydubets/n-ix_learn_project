import os
import csv
import subprocess
from flask import Flask, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from flask_restful import Resource, Api
from flask_login import LoginManager, login_required
from flask_migrate import Migrate
from .models import db, User, Film, Director, Genre
from sqlalchemy import select, engine, create_engine
from dotenv import load_dotenv
from sqlalchemy_utils import database_exists, create_database



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    api = Api(app)
    load_dotenv()
    SWAGGER_URL = os.getenv("SWAGGER_URL")
    API_URL = os.getenv("API_URL")
    swagger_ui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': 'Access API'
        }
    )
    if test_config is None:
        # load the instance config, if it exists, when not testing
        # app.config.from_pyfile('config.py', silent=True)
        app.config.from_mapping(
            SECRET_KEY=os.getenv("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.getenv("SQLALCHEMY_DATABASE_URI")
        )
    else:
        # load the test config if passed in
        #app.config.from_mapping(test_config)
        app.config.from_mapping(
            SECRET_KEY=os.getenv("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.getenv("SQLALCHEMY_DATABASE_URI")
        )

        # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    login_manager = LoginManager()
    login_manager.init_app(app)
    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)
    db.init_app(app)


    migrate = Migrate(app, db, 'films/migrations')


    @login_manager.user_loader
    def load_user():
        # since the user_id is just the primary key of our user table, use it in the query for the user
        pass


    class HelloWorld(Resource):
        def get(self):
            return 'Hello, world!  '+str(os.getenv("SQLALCHEMY_DATABASE_URI")), 200


    class HelloThere(Resource):
        def get(self):
            subprocess.run(["flask", "db", "upgrade"])
            subprocess.run(["flask", "db", "migrate"])
            subprocess.run(["flask", "db", "upgrade"])
            subprocess.run(["flask", "seed"])
            return 'Hello, world!', 200


    class Films(Resource):
        #@login_required
        def get(self):
            print(os.getenv("TEST_SQLALCHEMY_DATABASE_URI"))
            all_films = db.session.query(Film).order_by(Film.film_id).all()
            for item in all_films:
                print(item.film_id, item.name, item.rating, "./static/"+item.poster+".jpg")
            return {"app_name": "films"}, 200

        def post(self):
            return {"app_name": request.get_json()["app_name"]}, 200


    api.add_resource(Films, "/api/films")
    api.add_resource(HelloWorld, "/api/hello")
    api.add_resource(HelloThere, "/api/seed")


    def seed_from_file_decorator(function):
        def wrapper(*args, **kwargs):
            result = function(*args, **kwargs)
            file = open(result[0], "r")
            data = list(csv.reader(file, delimiter=","))

            file.close()
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
        elif table == 'Directors':
            return file, Director.__table__.columns.keys(), Director
        elif table == 'Genres':
            return file, Genre.__table__.columns.keys(), Genre
        elif table == 'Films':
            return file, Film.__table__.columns.keys(), Film



    @app.cli.command('seed')
    def seed():
        with app.app_context():
            seed_from_file("./tests/directors_mock.csv", 'Directors')
            seed_from_file("./tests/users_mock.csv", 'Users')
            seed_from_file("./tests/genres_mock.csv", 'Genres')
            seed_from_file("./tests/films_mock.csv", 'Films')


    return app