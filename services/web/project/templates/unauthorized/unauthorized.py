from flask import Blueprint, jsonify, request
from flask_restful import Resource, Api

unauthorized_api = Blueprint('unauthorized', __name__, template_folder='/unauthorized')
api = Api(unauthorized_api)

