from flask import Blueprint
from flask_restful import Api
from .LogInApi import LoginApi, LogoutApi, UserDataApi, RegisterApi

login_api = Blueprint('login', __name__, template_folder='/login')
api = Api(login_api)

api.add_resource(LoginApi, "/api/v1.0/login")
api.add_resource(LogoutApi, "/api/v1.0/logout")
api.add_resource(UserDataApi, "/api/v1.0/user")
api.add_resource(RegisterApi, "/api/v1.0/register")