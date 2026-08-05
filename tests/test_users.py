def test_register_user(client):
    response = client.post(
        "/register",
        json={"username": "testuser", "password": "testpassword"}
    )

    assert response.status_code == 200

    user = response.json()

    assert user["username"] == "testuser"
    assert user["id"] is not None
    assert "hashed_password" not in user


def test_register_existing_user(client):
    # First, register a user
    first_response = client.post(
        "/register",
        json={"username": "existinguser", "password": "testpassword"}
    )

    assert first_response.status_code == 200

    # Try to register the same user again
    response = client.post(
        "/register",
        json={"username": "existinguser", "password": "testpassword"}
    )

    assert response.status_code == 409
    assert response.json() == {"detail": "Username already exists"}


def test_register_user_empty_username(client):
    response = client.post(
        "/register",
        json={
            "username": "",
            "password": "testpassword"
        }
    )

    assert response.status_code == 422


def test_register_user_short_username(client):
    response = client.post(
        "/register",
        json={
            "username": "ab",
            "password": "testpassword"
        }
    )

    assert response.status_code == 422


def test_register_user_short_password(client):
    response = client.post(
        "/register",
        json={
            "username": "testuser",
            "password": "123"
        }
    )

    assert response.status_code == 422
