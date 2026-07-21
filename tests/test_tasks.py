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
