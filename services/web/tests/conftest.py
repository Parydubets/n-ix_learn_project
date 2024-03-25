import pytest
from dotenv import load_dotenv
from ..project import create_app
from ..project.models import db

@pytest.fixture()
def app():
    app = create_app(test_config="testing")
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()