def test_list_models(auth_client):
    resp = auth_client.get("/api/ai/models")
    assert resp.status_code == 200
    models = resp.get_json()["data"]
    assert len(models) > 0
    assert models[0]["id"] == "gpt-4o"


def test_list_conversations_empty(auth_client):
    resp = auth_client.get("/api/ai/conversations")
    assert resp.status_code == 200
    assert resp.get_json()["data"] == []


def test_playground_missing_prompt(auth_client):
    resp = auth_client.post("/api/ai/playground", json={})
    assert resp.status_code == 400


def test_chat_missing_message(auth_client):
    resp = auth_client.post("/api/ai/chat", json={})
    assert resp.status_code == 400


def test_ai_requires_auth(client):
    resp = client.get("/api/ai/models")
    assert resp.status_code == 401
