import os
from flask import Flask, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from flask_restful import Resource, Api
from flask_login import LoginManager, login_required
from flask_migrate import Migrate
from .models import db, User, Film

app = Flask(__name__)
api = Api(app)

SWAGGER_URL = os.getenv("SWAGGER_URL")
API_URL = os.getenv("API_URL")
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Access API'
    }
)
app.config.from_mapping(
    SECRET_KEY=os.getenv("SECRET_KEY"),
    SQLALCHEMY_DATABASE_URI=os.getenv("SQLALCHEMY_DATABASE_URI")
)
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
        return jsonify({'message': 'Hello, world!'})


class Films(Resource):
    @login_required
    def get(self):
        return {"app_name": "films"}, 200

    def post(self):
        return {"app_name": request.get_json()["app_name"]}, 200


api.add_resource(Films, "/api/app_name")
api.add_resource(HelloWorld, "/api/hello")
