from flask.testing import FlaskClient
from app import app
import models
import pytest

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_server_is_running(client: FlaskClient):
    response = client.get('/status')
    assert response.status_code == 200, "Server is not running"


# run tessts
# pytest test.py


