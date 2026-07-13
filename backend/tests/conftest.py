import pytest
from app import create_app
from app.extensions import db as _db


@pytest.fixture
def app():
    app = create_app("testing")
    with app.app_context():
        _db.create_all()
        yield app
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db_session(app):
    with app.app_context():
        yield _db.session


@pytest.fixture
def registered_user(client):
    resp = client.post("/api/auth/register", json={
        "email": "test@example.com",
        "password": "password123",
        "name": "Test User",
    })
    return resp.get_json()["data"]


@pytest.fixture
def auth_client(client, registered_user):
    client.post("/api/auth/login", json={
        "email": "test@example.com",
        "password": "password123",
    })
    return client
