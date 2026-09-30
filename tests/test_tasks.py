def test_create_task(client):
    """Test 2: Create a task successfully with valid payload."""
    payload = {"title": "Learn FastAPI", "description": "Build a Task Management API"}
    response = client.post("/tasks/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["title"] == "Learn FastAPI"
    assert data["description"] == "Build a Task Management API"
    assert data["is_completed"] is False
    assert "created_at" in data
    assert "updated_at" in data


def test_get_all_tasks_empty(client):
    """Test 3a: Get all tasks when database is empty."""
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert response.json() == []


def test_get_all_tasks_populated(client):
    """Test 3b: Get all tasks when tasks exist."""
    client.post("/tasks/", json={"title": "Task 1"})
    client.post("/tasks/", json={"title": "Task 2"})

    response = client.get("/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Task 1"
    assert data[1]["title"] == "Task 2"


def test_get_task_by_id_success(client):
    """Test 4: Get a single task by ID."""
    create_res = client.post("/tasks/", json={"title": "Specific Task"})
    task_id = create_res.json()["id"]

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Specific Task"


def test_get_nonexistent_task(client):
    """Test 5: Get a nonexistent task returns 404 Not Found."""
    response = client.get("/tasks/999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Task with ID 999 not found"


def test_update_task_success(client):
    """Test 6a: Update an existing task."""
    create_res = client.post(
        "/tasks/", json={"title": "Initial Title", "description": "Initial Desc"}
    )
    task_id = create_res.json()["id"]

    update_payload = {"title": "Updated Title", "description": "Updated Desc"}
    response = client.put(f"/tasks/{task_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Updated Title"
    assert data["description"] == "Updated Desc"


def test_update_nonexistent_task(client):
    """Test 6b: Update a nonexistent task returns 404 Not Found."""
    response = client.put("/tasks/999", json={"title": "Non-existent Task"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Task with ID 999 not found"


def test_delete_task_success(client):
    """Test 7: Delete an existing task returns 204 No Content."""
    create_res = client.post("/tasks/", json={"title": "Task to Delete"})
    task_id = create_res.json()["id"]

    delete_res = client.delete(f"/tasks/{task_id}")
    assert delete_res.status_code == 204

    # Verify task is deleted
    get_res = client.get(f"/tasks/{task_id}")
    assert get_res.status_code == 404


def test_delete_nonexistent_task(client):
    """Test 8: Delete a nonexistent task returns 404 Not Found."""
    response = client.delete("/tasks/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task with ID 999 not found"


def test_mark_task_as_completed_success(client):
    """Test 9: Mark an existing task as completed."""
    create_res = client.post("/tasks/", json={"title": "Incomplete Task"})
    task_id = create_res.json()["id"]
    assert create_res.json()["is_completed"] is False

    patch_res = client.patch(f"/tasks/{task_id}/complete")
    assert patch_res.status_code == 200
    data = patch_res.json()
    assert data["id"] == task_id
    assert data["is_completed"] is True


def test_mark_nonexistent_task_as_completed(client):
    """Test 10: Mark a nonexistent task as completed returns 404 Not Found."""
    response = client.patch("/tasks/999/complete")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task with ID 999 not found"


def test_filter_completed_tasks(client):
    """Test 11: Filter completed tasks using ?completed=true."""
    client.post("/tasks/", json={"title": "Pending Task"})
    res2 = client.post("/tasks/", json={"title": "Finished Task"})
    task2_id = res2.json()["id"]
    client.patch(f"/tasks/{task2_id}/complete")

    res_true = client.get("/tasks/?completed=true")
    assert res_true.status_code == 200
    tasks_true = res_true.json()
    assert len(tasks_true) == 1
    assert tasks_true[0]["title"] == "Finished Task"
    assert tasks_true[0]["is_completed"] is True


def test_filter_incomplete_tasks(client):
    """Test 12: Filter incomplete tasks using ?completed=false."""
    client.post("/tasks/", json={"title": "Pending Task"})
    res2 = client.post("/tasks/", json={"title": "Finished Task"})
    task2_id = res2.json()["id"]
    client.patch(f"/tasks/{task2_id}/complete")

    res_false = client.get("/tasks/?completed=false")
    assert res_false.status_code == 200
    tasks_false = res_false.json()
    assert len(tasks_false) == 1
    assert tasks_false[0]["title"] == "Pending Task"
    assert tasks_false[0]["is_completed"] is False


def test_validation_error_missing_title(client):
    """Test 13a: Validation error when title is missing."""
    response = client.post("/tasks/", json={"description": "No title provided"})
    assert response.status_code == 422


def test_validation_error_empty_title(client):
    """Test 13b: Validation error when title is an empty string."""
    response = client.post("/tasks/", json={"title": ""})
    assert response.status_code == 422


def test_validation_error_title_too_long(client):
    """Test 13c: Validation error when title exceeds 255 characters."""
    long_title = "a" * 256
    response = client.post("/tasks/", json={"title": long_title})
    assert response.status_code == 422


def test_validation_error_invalid_query_param(client):
    """Test 13d: Validation error when query param 'completed' is invalid type."""
    response = client.get("/tasks/?completed=invalid_boolean")
    assert response.status_code == 422
