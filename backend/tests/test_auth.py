from unittest.mock import patch, MagicMock


def test_register_success(client):
    resp = client.post("/api/auth/register", json={
        "email": "new@example.com",
        "password": "password123",
        "name": "New User",
    })
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["success"] is True
    assert data["data"]["email"] == "new@example.com"


def test_register_duplicate(client, registered_user):
    resp = client.post("/api/auth/register", json={
        "email": "test@example.com",
        "password": "password123",
        "name": "Dup User",
    })
    assert resp.status_code == 409


def test_register_missing_fields(client):
    resp = client.post("/api/auth/register", json={"email": "a@b.com"})
    assert resp.status_code == 400


def test_login_success(client, registered_user):
    resp = client.post("/api/auth/login", json={
        "email": "test@example.com",
        "password": "password123",
    })
    assert resp.status_code == 200
    assert resp.get_json()["success"] is True


def test_login_wrong_password(client, registered_user):
    resp = client.post("/api/auth/login", json={
        "email": "test@example.com",
        "password": "wrongpass",
    })
    assert resp.status_code == 401


def test_me_authenticated(auth_client):
    resp = auth_client.get("/api/auth/me")
    assert resp.status_code == 200
    assert resp.get_json()["data"]["email"] == "test@example.com"


def test_me_unauthenticated(client):
    resp = client.get("/api/auth/me")
    assert resp.status_code == 401


def test_logout(auth_client):
    resp = auth_client.post("/api/auth/logout")
    assert resp.status_code == 200
    resp2 = auth_client.get("/api/auth/me")
    assert resp2.status_code == 401


def test_health(client):
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"


def test_google_login_missing_token(client):
    resp = client.post("/api/auth/google", json={})
    assert resp.status_code == 400


def test_google_login_invalid_token(client):
    mock_resp = MagicMock()
    mock_resp.status_code = 401
    with patch("app.auth.routes.requests.get", return_value=mock_resp):
        resp = client.post("/api/auth/google", json={"token": "bad-token"})
    assert resp.status_code == 401


def test_google_login_success(client):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "sub": "google-uid-123",
        "email": "google@example.com",
        "name": "Google User",
        "picture": "https://example.com/photo.jpg",
    }
    with patch("app.auth.routes.requests.get", return_value=mock_resp):
        resp = client.post("/api/auth/google", json={"token": "valid-token"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["success"] is True
    assert data["data"]["email"] == "google@example.com"
    assert data["data"]["name"] == "Google User"
