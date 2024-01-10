from flask.testing import FlaskClient
from app import app
import models
import pytest

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client
    
@pytest.fixture
def reset_db():
    models.db.drop_all()
    models.db.create_all()
    yield
    models.db.drop_all()

def test_server_is_running(client: FlaskClient):
    response = client.get('/status')
    assert response.status_code == 200, "Server is not running"

def test_fun():
    assert True
