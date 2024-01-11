"""
This contains all the tests for the server.
"""
import models
import pytest
from app import app
from flask.testing import FlaskClient


@pytest.fixture
def testing_client():
    """
    This fixture creates a test client for the server.
    """
    with app.test_client() as client:
        yield client


@pytest.fixture
def reset_db():
    """
    Resets the database to a clean state.
    """
    models.db.drop_all()
    models.db.create_all()
    yield
    models.db.drop_all()


def test_server_is_running(client: FlaskClient):
    """
    This test checks that the server is running.
    """
    response = client.get('/status')
    assert response.status_code == 200, "Server is not running"
