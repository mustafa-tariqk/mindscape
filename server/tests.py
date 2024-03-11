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


def test_converse(fake_client: FlaskClient):
    """
    Test the converse route
    """
    response = fake_client.post('/converse', json={'chat_id': 1, 'message': 'Hello'})
    assert response.status_code == 200
    data = response.get_json()
    assert 'ai_response' in data


def test_change_permission(fake_client: FlaskClient):
    """
    Test the change permission route
    """
    response = fake_client.get('/change_permission/1/Administrator')
    assert response.status_code == 200
    data = response.get_json()
    assert 'role' in data and data['role'] == 'Administrator'


def test_flag_chat(fake_client: FlaskClient):
    """
    Test the flag chat route
    """
    response = fake_client.get('/flag/1')
    assert response.status_code == 200
    data = response.get_json()
    assert 'status' in data and data['status'] == 'flagged'

def test_get_trolls(fake_client: FlaskClient):
    """
    Test the get trolls route
    """
    response = fake_client.get('/get_trolls')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, dict)


def test_get_all_chats(fake_client: FlaskClient):
    """
    Test the get all chats route
    """
    response = fake_client.get('/get_all_chats')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, dict)


def test_delete_chat(fake_client: FlaskClient):
    """
    Test the delete chat route
    """
    response = fake_client.get('/delete_chat/1')
    assert response.status_code == 200
    data = response.get_json()
    assert 'status' in data and data['status'] == 'deleted'


def test_delete_user(fake_client: FlaskClient):
    """
    Test the delete user route, has to be run last.
    """
    response = fake_client.get('/delete_user/1')
    assert response.status_code == 200
    data = response.get_json()
    assert 'status' in data and data['status'] == 'deleted'