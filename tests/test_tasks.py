def test_create_task(client):
    response = client.post(
        "/tasks",
        json={"title": "Test Task creation"}
    )

    assert response.status_code == 200

    task = response.json()

    assert task["title"] == "Test Task creation"
    assert task["completed"] is False
