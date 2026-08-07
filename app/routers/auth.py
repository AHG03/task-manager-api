from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models import User
from app.schemas import LoginResponse, UserLogin
from app.security import verify_password

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(
        User.username == user.username).first()

    if existing_user is None:
        raise HTTPException(
            status_code=401, detail="Invalid username or password")

    if not verify_password(user.password, existing_user.hashed_password):
        raise HTTPException(
            status_code=401, detail="Invalid username or password")

    return {"message": "Login successful"}
