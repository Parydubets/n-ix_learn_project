import logging
from flask_restful import Resource
from flask import request, current_app
from ...service import get_user_data, set_user_password
from ...models import db, User, users
from flask_login import login_user, logout_user, current_user,login_required
from werkzeug.security import generate_password_hash, check_password_hash

logger = logging.getLogger('app.project.my_tool')

class LoginApi(Resource):
    def post(self):
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        user = User.query.filter(User.email == email).first()
        if not user or not check_password_hash(user.password, password):
            current_app.logger.warning("Wrong credentials")
            return {"message": "wrong credentials."}, 401  # if the user doesn't exist or password is wrong, reload the page

        login_user(user, remember=remember)
        current_app.logger.warning("successfully logged")
        return {"message": "successfully logged"}, 200


class RegisterApi(Resource):
    def post(self):
        current_app.logger.info("Registering user with email {}".format(request.form.get('email')))
        email= request.form.get('email')
        password= request.form.get('password')
        first_name= request.form.get('first_name')
        last_name= request.form.get('last_name')
        phone = request.form.get('phone')
        is_admin= False


        user = User.query.filter_by(email=email).first()

        if user:
            current_app.logger.warning("User already exists")
            return {"message": "user already exists"}, 400

        new_user = User(email=email, password=generate_password_hash(password),
                        first_name=first_name, last_name=last_name, phone=phone, is_admin=is_admin)

        db.session.add(new_user)
        db.session.commit()
        current_app.logger.info("Successfully registered")
        return {"message": "successfully registered"}, 200


class LogoutApi(Resource):
    @login_required
    def get(self):
        current_app.logger.info("Logging out")
        id = current_user.id
        current_user.isauthenticated = False
        db.session.commit()
        logout_user()
        current_app.logger.info("Logged out user with id={}".format(id))
        return {"message": "logged out user with id={}".format(id)}, 200


class UserDataApi(Resource):
    @login_required
    def get(self):
        current_app.logger.info("Getting current user (id={}) data".format(current_user.id))
        return get_user_data(), 200


    @login_required
    def post(self):
        current_app.logger.info("Changing user (id={}) password".format(current_user.id))
        passwords = [request.form.get('password'), request.form.get('new_password_1'), request.form.get("new_password_2")]
        if passwords[1] == passwords[2] and check_password_hash(current_user.password, passwords[0]):
            set_user_password(passwords[1])
            current_app.logger.info("Successfully changed password")
            return {"message": "successfully changed password"}, 200
        elif passwords[1] != passwords[2]:
            current_app.logger.info("New password fields aren't identical")
            return {"error": "new password fields aren't identical"}, 400
        elif check_password_hash(current_user.password, passwords[0]) is False:
            current_app.logger.info("Wrong password")
            return {"error": "wrong password"}, 400