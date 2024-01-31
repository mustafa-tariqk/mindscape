"""
This contains all the tests for the server.
"""
import pytest
from flask.testing import FlaskClient
import models
from app import app


@pytest.fixture
def fake_client():
    """
    This fixture creates a test client for the server.
    """
    with app.app_context():
        with app.test_client() as test_client:
            yield test_client


@pytest.fixture
def reset_db():
    """
    Resets the database to a clean state.
    """
    models.db.drop_all()
    models.db.create_all()
    yield
    models.db.drop_all()


def test_index(fake_client: FlaskClient):
    """
    Ensures the redirect to Google login works.
    """
    response = fake_client.get("/")
    assert response.status_code == 302  # Expecting a redirect to Google login
