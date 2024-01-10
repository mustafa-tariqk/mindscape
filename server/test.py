from flask.testing import FlaskClient
import app, models
import pytest

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_server_is_running(client: FlaskClient):
    response = client.get('/')
    assert response.status_code == 200, "Server is not running"


# run tessts
# pytest test.py


