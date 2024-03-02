from flask_restful import Resource
from flask import request


class LoginApi(Resource):
    def post(self):
        print(request.json.get("email").strip())
        print(request.json.get("password").strip())
        return {"message": "This is the endpoint for log in"}, 200


class RegisterApi(Resource):
    def post(self):
        data = request.json
        for parameter in data:
            print(data[parameter])
        return {"message": "This is the endpoint for registration"}, 200


class LogoutApi(Resource):
    def get(self):
        return {"message": "This is the endpoint for logout"}, 200


class UserDataApi(Resource):
    def get(self):
        return {"message": "This endpoint displays user data"}, 200

    def post(self):
        return {"message": "This endpoint changes the password"}, 200
