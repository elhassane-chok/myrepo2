def test_create_task(auth_client):
    resp = auth_client.post("/api/tasks", json={"title": "My Task"})
    assert resp.status_code == 201
    data = resp.get_json()["data"]
    assert data["title"] == "My Task"
    assert data["status"] == "todo"
    assert data["priority"] == "medium"


def test_list_tasks(auth_client):
    auth_client.post("/api/tasks", json={"title": "Task 1"})
    auth_client.post("/api/tasks", json={"title": "Task 2"})
    resp = auth_client.get("/api/tasks")
    assert resp.status_code == 200
    assert len(resp.get_json()["data"]) == 2


def test_get_task(auth_client):
    create_resp = auth_client.post("/api/tasks", json={"title": "Get Me"})
    task_id = create_resp.get_json()["data"]["id"]
    resp = auth_client.get(f"/api/tasks/{task_id}")
    assert resp.status_code == 200
    assert resp.get_json()["data"]["title"] == "Get Me"


def test_update_task(auth_client):
    create_resp = auth_client.post("/api/tasks", json={"title": "Old Title"})
    task_id = create_resp.get_json()["data"]["id"]
    resp = auth_client.put(f"/api/tasks/{task_id}", json={"title": "New Title", "status": "in_progress"})
    assert resp.status_code == 200
    assert resp.get_json()["data"]["title"] == "New Title"
    assert resp.get_json()["data"]["status"] == "in_progress"


def test_delete_task(auth_client):
    create_resp = auth_client.post("/api/tasks", json={"title": "Delete Me"})
    task_id = create_resp.get_json()["data"]["id"]
    resp = auth_client.delete(f"/api/tasks/{task_id}")
    assert resp.status_code == 200
    resp2 = auth_client.get(f"/api/tasks/{task_id}")
    assert resp2.status_code == 404


def test_filter_by_status(auth_client):
    auth_client.post("/api/tasks", json={"title": "A", "status": "done"})
    auth_client.post("/api/tasks", json={"title": "B", "status": "todo"})
    resp = auth_client.get("/api/tasks?status=done")
    assert len(resp.get_json()["data"]) == 1


def test_create_project(auth_client):
    resp = auth_client.post("/api/projects", json={"name": "My Project"})
    assert resp.status_code == 201
    assert resp.get_json()["data"]["name"] == "My Project"


def test_list_projects(auth_client):
    auth_client.post("/api/projects", json={"name": "P1"})
    resp = auth_client.get("/api/projects")
    assert resp.status_code == 200
    assert len(resp.get_json()["data"]) == 1


def test_delete_project(auth_client):
    create_resp = auth_client.post("/api/projects", json={"name": "Del"})
    pid = create_resp.get_json()["data"]["id"]
    resp = auth_client.delete(f"/api/projects/{pid}")
    assert resp.status_code == 200


def test_task_requires_auth(client):
    resp = client.get("/api/tasks")
    assert resp.status_code == 401
