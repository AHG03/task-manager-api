def test_create_task(client):
    response = client.post(
        "/tasks",
        json={"title": "Test Task creation"}
    )

    assert response.status_code == 200

    task = response.json()

    assert task["title"] == "Test Task creation"
    assert task["completed"] is False


def test_get_tasks_empty(client):
    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == []


def test_get_missing_task(client):
    response = client.get("/tasks/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_create_task_empty_title(client):
    response = client.post(
        "/tasks",
        json={"title": ""}
    )

    assert response.status_code == 422


def test_create_task_whitespace_title(client):
    response = client.post(
        "/tasks",
        json={"title": "     "}
    )

    assert response.status_code == 422


def test_update_task(client):
    response = client.post(
        "/tasks",
        json={"title": "Original title"}
    )

    task = response.json()
    task_id = task["id"]

    response = client.put(
        f"/tasks/{task_id}",
        json={
            "title": "Updated title",
            "completed": True
        }
    )

    assert response.status_code == 200

    updated_task = response.json()

    assert updated_task["title"] == "Updated title"
    assert updated_task["completed"] is True


def test_patch_task(client):
    response = client.post(
        "/tasks",
        json={"title": "Original title"}
    )

    task = response.json()
    task_id = task["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={"completed": True}
    )

    assert response.status_code == 200

    updated_task = response.json()

    assert updated_task["title"] == "Original title"
    assert updated_task["completed"] is True


def test_delete_task(client):
    response = client.post(
        "/tasks",
        json={"title": "Original task"}
    )

    task = response.json()
    task_id = task["id"]

    response = client.delete(f"/tasks/{task_id}")

    assert response.status_code == 200
    assert response.json()["message"] == "Task deleted successfully"

    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_get_tasks_with_completed_filter(client):
    # Create tasks
    client.post("/tasks", json={"title": "Task 1"})
    task_2 = client.post("/tasks", json={"title": "Task 2"}).json()
    client.post("/tasks", json={"title": "Task 3"})

    # Update Task 2 to be completed
    client.put(
        f"/tasks/{task_2['id']}",
        json={"title": "Task 2", "completed": True}
    )

    # Get tasks with completed=True
    response = client.get("/tasks?completed=true")

    assert response.status_code == 200

    completed_tasks = response.json()

    assert len(completed_tasks) == 1
    assert completed_tasks[0]["title"] == "Task 2"
    assert completed_tasks[0]["completed"] is True


def test_get_tasks_with_incomplete_filter(client):
    # Create tasks
    client.post("/tasks", json={"title": "Task 1"})
    task_2 = client.post("/tasks", json={"title": "Task 2"}).json()
    client.post("/tasks", json={"title": "Task 3"})

    # Update Task 2 to be completed
    client.put(
        f"/tasks/{task_2['id']}",
        json={"title": "Task 2", "completed": True}
    )

    # Get tasks with completed=False
    response = client.get("/tasks?completed=false")

    assert response.status_code == 200

    incomplete_tasks = response.json()

    assert len(incomplete_tasks) == 2

    titles = {task["title"] for task in incomplete_tasks}

    assert titles == {"Task 1", "Task 3"}

    for task in incomplete_tasks:
        assert task["completed"] is False
