import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from app.dependencies import get_current_user
from app.security import create_access_token


def test_login_success(client):
    # First, register a user
    register_response = client.post(
        "/register",
        json={"username": "testuser", "password": "testpassword"}
    )

    assert register_response.status_code == 200

    # Now, attempt to log in with the registered user
    response = client.post(
        "/login",
        json={"username": "testuser", "password": "testpassword"}
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["access_token"]
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    # First, register a user
    register_response = client.post(
        "/register",
        json={"username": "testuser", "password": "testpassword"}
    )

    assert register_response.status_code == 200

    # Now, attempt to log in with the wrong password
    response = client.post(
        "/login",
        json={"username": "testuser", "password": "wrongpassword"}
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid username or password"}


def test_login_nonexistent_user(client):
    # Attempt to log in with a username that doesn't exist
    response = client.post(
        "/login",
        json={"username": "nonexistentuser", "password": "any_password"}
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid username or password"}


def test_get_current_user(client, db):
    client.post(
        "/register",
        json={
            "username": "testuser",
            "password": "testpassword"
        }
    )

    token = create_access_token({"sub": "testuser"})

    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials=token
    )

    user = get_current_user(credentials, db)

    assert user.username == "testuser"


def test_get_current_user_invalid_token(client, db):
    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials="this-is-not-a-valid-token"
    )

    with pytest.raises(HTTPException) as exc_info:
        get_current_user(credentials, db)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Could not validate credentials"


def test_get_current_user_nonexistent_user(client, db):
    token = create_access_token({"sub": "doesnotexist"})

    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials=token
    )

    with pytest.raises(HTTPException) as exc_info:
        get_current_user(credentials, db)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Could not validate credentials"
