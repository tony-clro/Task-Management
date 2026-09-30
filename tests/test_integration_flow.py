"""
Integration verification script testing the exact frontend-backend user flow.
Simulates the JavaScript fetch API calls made by static/app.js.
"""

def test_full_frontend_backend_user_flow(client):
    # 1. Load tasks (Initial load & static page check)
    page_res = client.get("/app/")
    assert page_res.status_code == 200
    assert "Task Management API" in page_res.text

    init_res = client.get("/tasks/")
    assert init_res.status_code == 200

    # 2. Create a task (POST /tasks/)
    create_payload = {
        "title": "Test Frontend Integration Task",
        "description": "Testing complete end-to-end integration flow",
    }
    create_res = client.post("/tasks/", json=create_payload)
    assert create_res.status_code == 201
    task_data = create_res.json()
    task_id = task_data["id"]
    assert task_data["title"] == "Test Frontend Integration Task"
    assert task_data["is_completed"] is False

    # 3. Retrieve/display the task (GET /tasks/{task_id})
    get_res = client.get(f"/tasks/{task_id}")
    assert get_res.status_code == 200
    assert get_res.json()["id"] == task_id

    # 4. Edit the task (PUT /tasks/{task_id})
    edit_payload = {
        "title": "Updated Frontend Integration Task",
        "description": "Updated integration description",
        "is_completed": False,
    }
    edit_res = client.put(f"/tasks/{task_id}", json=edit_payload)
    assert edit_res.status_code == 200
    assert edit_res.json()["title"] == "Updated Frontend Integration Task"

    # 5. Mark it completed (PATCH /tasks/{task_id}/complete)
    complete_res = client.patch(f"/tasks/{task_id}/complete")
    assert complete_res.status_code == 200
    assert complete_res.json()["is_completed"] is True

    # 6. Filter completed tasks (GET /tasks/?completed=true)
    completed_res = client.get("/tasks/?completed=true")
    assert completed_res.status_code == 200
    completed_tasks = completed_res.json()
    assert any(t["id"] == task_id for t in completed_tasks)

    # 7. Filter pending tasks (GET /tasks/?completed=false)
    pending_res = client.get("/tasks/?completed=false")
    assert pending_res.status_code == 200
    pending_tasks = pending_res.json()
    assert not any(t["id"] == task_id for t in pending_tasks)

    # 8. Delete the task (DELETE /tasks/{task_id})
    delete_res = client.delete(f"/tasks/{task_id}")
    assert delete_res.status_code == 204

    # Confirm deletion
    verify_delete_res = client.get(f"/tasks/{task_id}")
    assert verify_delete_res.status_code == 404
