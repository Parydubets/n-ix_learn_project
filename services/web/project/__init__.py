""" The project init """
import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask import has_request_context, request
from flask_swagger_ui import get_swaggerui_blueprint
from flask_restful import Api
from flask_migrate import Migrate
from dotenv import load_dotenv
from .models import db, User, Film, Director, Genre
from .blueprints.films import films_api
from .blueprints.directors import directors_api
from .blueprints.login import login_api
from .blueprints.genres import genres_api
from flask_marshmallow import Marshmallow
from .config import Config, Config_Test
from flask_login import LoginManager

login_manager = LoginManager()

def create_app(config=Config):
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

    app.config.from_object(config)

    migrate = Migrate(app, db, 'project/migrations')
    db.init_app(app)
    login_manager.init_app(app)
    ma = Marshmallow()
    ma.init_app(app)

    @app.route('/halo')
    def halo():
        return "halo"

    @app.route('/haloo')
    def haloo():
        return {"message": "halo"}, 200

    class RequestFormatter(logging.Formatter):
        def format(self, record):
            if has_request_context():
                record.url = request.url
                record.remote_addr = request.remote_addr
                record.method = request.method
            else:
                record.url = None
                record.remote_addr = None

            return super().format(record)
    handler = logging.handlers.RotatingFileHandler('app.log', maxBytes=1024 * 1024)
    formatter = RequestFormatter(
        '[%(asctime)s] %(remote_addr)s  requested %(method)s %(url)s\n'
        '%(levelname)s in %(module)s: %(message)s'
    )
    handler.setFormatter(formatter)
    logger = logging.getLogger('werkzeug')
    logger.setLevel(logging.INFO)

    app.logger.addHandler(handler)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.where(User.id == int(user_id)).first()



    app.register_blueprint(swagger_ui_blueprint, url_prefix=os.getenv("SWAGGER_URL"))
    app.register_blueprint(films_api)
    app.register_blueprint(directors_api)
    app.register_blueprint(login_api)
    app.register_blueprint(genres_api)

    return app


"""    @login_manager.unauthorized_handler
    def unauthorized():
        # do stuff
        return {"message":"login first"}"""