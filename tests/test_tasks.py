def get_auth_headers(client):
    client.post(
        "/register",
        json={
            "username": "testuser",
            "password": "testpassword"
        }
    )

    response = client.post(
        "/login",
        json={
            "username": "testuser",
            "password": "testpassword"
        }
    )

    token = response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}


def create_sample_tasks(client, count, headers):
    for i in range(count):
        client.post("/tasks", json={"title": f"Task {i + 1}"}, headers=headers)


def test_create_task(client):
    headers = get_auth_headers(client)

    response = client.post(
        "/tasks",
        json={"title": "Test Task creation"},
        headers=headers
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
    headers = get_auth_headers(client)

    response = client.post(
        "/tasks",
        json={"title": ""},
        headers=headers
    )

    assert response.status_code == 422


def test_create_task_whitespace_title(client):
    headers = get_auth_headers(client)

    response = client.post(
        "/tasks",
        json={"title": "     "},
        headers=headers
    )

    assert response.status_code == 422


def test_update_task(client):
    headers = get_auth_headers(client)

    response = client.post(
        "/tasks",
        json={"title": "Original title"},
        headers=headers
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
    headers = get_auth_headers(client)

    response = client.post(
        "/tasks",
        json={"title": "Original title"},
        headers=headers
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
    headers = get_auth_headers(client)

    response = client.post(
        "/tasks",
        json={"title": "Original task"},
        headers=headers
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
    headers = get_auth_headers(client)

    client.post("/tasks", json={"title": "Task 1"}, headers=headers)
    task_2 = client.post(
        "/tasks", json={"title": "Task 2"}, headers=headers).json()
    client.post("/tasks", json={"title": "Task 3"}, headers=headers)

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
    headers = get_auth_headers(client)

    client.post("/tasks", json={"title": "Task 1"}, headers=headers)
    task_2 = client.post(
        "/tasks", json={"title": "Task 2"}, headers=headers).json()
    client.post("/tasks", json={"title": "Task 3"}, headers=headers)

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


def test_get_tasks_with_search_filter(client):
    # Create tasks
    headers = get_auth_headers(client)

    client.post("/tasks", json={"title": "Buy milk"}, headers=headers)
    client.post("/tasks", json={"title": "Do laundry"}, headers=headers)
    client.post("/tasks", json={"title": "Milk the cow"}, headers=headers)

    # Get tasks with search filter
    response = client.get("/tasks?search=milk")
    assert response.status_code == 200
    tasks = response.json()

    assert len(tasks) == 2
    titles = {task["title"] for task in tasks}
    assert titles == {"Buy milk", "Milk the cow"}


def test_get_tasks_with_search_no_results(client):
    # Create tasks
    client.post("/tasks", json={"title": "Buy milk"})
    client.post("/tasks", json={"title": "Do laundry"})
    client.post("/tasks", json={"title": "Milk the cow"})

    # Get tasks with search filter that yields no results
    response = client.get("/tasks?search=eggs")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 0


def test_get_tasks_with_search_and_completed_filter(client):
    headers = get_auth_headers(client)

    client.post("/tasks", json={"title": "Buy milk"}, headers=headers)
    client.post("/tasks", json={"title": "Milk the cow"}, headers=headers)
    task = client.post(
        "/tasks", json={"title": "Buy milk tomorrow"}, headers=headers).json()
    client.put(
        f"/tasks/{task['id']}", json={"title": "Buy milk tomorrow", "completed": True})

    response = client.get("/tasks?search=milk&completed=true")

    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Buy milk tomorrow"
    assert tasks[0]["completed"] is True


def test_get_tasks_sort_by_title_ascending(client):
    headers = get_auth_headers(client)

    client.post("/tasks", json={"title": "Zebra"}, headers=headers)
    client.post("/tasks", json={"title": "Apple"}, headers=headers)
    client.post("/tasks", json={"title": "Monkey"}, headers=headers)

    response = client.get("/tasks?sort_by=title")

    assert response.status_code == 200

    tasks = response.json()

    assert tasks[0]["title"] == "Apple"
    assert tasks[1]["title"] == "Monkey"
    assert tasks[2]["title"] == "Zebra"


def test_get_tasks_sort_by_title_descending(client):
    headers = get_auth_headers(client)

    client.post("/tasks", json={"title": "Zebra"}, headers=headers)
    client.post("/tasks", json={"title": "Apple"}, headers=headers)
    client.post("/tasks", json={"title": "Monkey"}, headers=headers)

    response = client.get(
        "/tasks?sort_by=title&sort_order=desc"
    )

    assert response.status_code == 200

    tasks = response.json()

    assert tasks[0]["title"] == "Zebra"
    assert tasks[1]["title"] == "Monkey"
    assert tasks[2]["title"] == "Apple"


def test_invalid_sort_field(client):
    response = client.get("/tasks?sort_by=random")

    assert response.status_code == 422


def test_invalid_sort_order(client):
    response = client.get(
        "/tasks?sort_by=title&sort_order=random"
    )

    assert response.status_code == 422


def test_get_tasks_with_limit(client):
    headers = get_auth_headers(client)

    create_sample_tasks(client, 3, headers)

    response = client.get("/tasks?limit=2")

    assert response.status_code == 200

    tasks = response.json()

    assert len(tasks) == 2
    assert tasks[0]["title"] == "Task 1"
    assert tasks[1]["title"] == "Task 2"


def test_get_tasks_with_limit_and_offset(client):
    headers = get_auth_headers(client)

    create_sample_tasks(client, 3, headers)

    response = client.get("/tasks?limit=2&offset=1")

    assert response.status_code == 200

    tasks = response.json()

    assert len(tasks) == 2
    assert tasks[0]["title"] == "Task 2"
    assert tasks[1]["title"] == "Task 3"


def test_get_tasks_invalid_limit(client):
    response = client.get("/tasks?limit=0")

    assert response.status_code == 422


def test_get_tasks_invalid_offset(client):
    response = client.get("/tasks?offset=-1")

    assert response.status_code == 422
