"""
This contains all the tests for the server.
"""
import pytest
from flask.testing import FlaskClient
import models
from app import app
from unittest.mock import patch

@pytest.fixture
def fake_client():
    """
    This fixture creates a test client for the server and mocks authentication.
    """
    app.config['TESTING'] = True
    with app.test_client() as test_client:
        yield test_client  # Yield the test client after patching


@pytest.fixture
def reset_db():
    """
    Resets the database to a clean state.
    """
    models.db.drop_all()
    models.db.create_all()
    yield
    models.db.drop_all()


def test_start_chat(fake_client: FlaskClient):
    """
    Example test using a client with mocked authentication
    """
    response = fake_client.get('/start_chat/1')
    assert response.status_code == 200
    data = response.get_json()
    assert 'chat_id' in data
