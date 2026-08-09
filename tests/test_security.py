import pytest
import jwt
from datetime import datetime, timedelta, timezone

from app.security import SECRET_KEY, create_access_token, decode_access_token


def test_create_and_decode_access_token():
    data = {"sub": "testuser"}
    token = create_access_token(data)
    decoded_data = decode_access_token(token)
    assert decoded_data["sub"] == "testuser"


def test_decode_invalid_token():
    token = jwt.encode({"sub": "testuser"},
                       "different_secret_key_that_is_long_enough_for_hs256",
                       algorithm="HS256")

    with pytest.raises(jwt.InvalidTokenError):
        decode_access_token(token)


def test_decode_expired_token():
    token = jwt.encode(
        {
            "sub": "testuser",
            "exp": datetime.now(timezone.utc) - timedelta(minutes=1)
        },
        SECRET_KEY,
        algorithm="HS256"
    )

    with pytest.raises(jwt.ExpiredSignatureError):
        decode_access_token(token)
