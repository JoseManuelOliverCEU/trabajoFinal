import os
import sys
import pytest
from app import create_app
from app.extensions import db

sys.path.append("/app")

@pytest.fixture()
def app():
    app = create_app()
    app.config.update(
        TESTING=True,
    )
    with app.app_context():
        yield app

@pytest.fixture()
def client(app):
    return app.test_client()
