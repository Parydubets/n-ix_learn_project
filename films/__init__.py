import os
from flask import Flask, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint


app = Flask(__name__)

SWAGGER_URL = os.getenv("SWAGGER_URL")
API_URL = os.getenv("API_URL")
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Access API'
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)



@app.route('/')
def hello():
    return jsonify({"Message":"Hello world"}), 200


@app.route("/app_name", methods=['GET', 'POST'])
def app_name():
    if request.method == "GET":
        return jsonify({
            "app_name": "films"
        }), 200
    if request.method == "POST":
        app_name = request.get_json()["app_name"]
        return jsonify({"app_name": app_name}), 200