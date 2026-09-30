def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert "message" in data
    assert "docs_url" in data
    assert "frontend_url" in data


def test_frontend_static_served(client):
    response = client.get("/app/")
    assert response.status_code == 200
    assert "Task Management API" in response.text
    assert "createTaskForm" in response.text
