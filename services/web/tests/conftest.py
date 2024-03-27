import pytest
from dotenv import load_dotenv
from ..project import create_app
from ..project.models import db
from ..project.config import Config_Test, Config

@pytest.fixture()
def app():
    app = create_app(config=Config_Test)
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()