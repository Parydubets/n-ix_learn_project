import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    load_dotenv("../../.env.dev")
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    MEDIA_FOLDER = f"./project/static/"

class Config_Test(object):
    load_dotenv("../../.env.dev")
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    MEDIA_FOLDER = f"{os.getenv('APP_FOLDER')}/project/media"