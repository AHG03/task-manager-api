import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.security import decode_access_token
from app.database import SessionLocal
from app.models import User


security = HTTPBearer()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security),
                     db: Session = Depends(get_db)):
    token = credentials.credentials

    try:
        payload = decode_access_token(token)
    except jwt.InvalidTokenError as exc:
        raise HTTPException(
            status_code=401, detail="Could not validate credentials") from exc

    username = payload["sub"]

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(
            status_code=401, detail="Could not validate credentials")

    return user
