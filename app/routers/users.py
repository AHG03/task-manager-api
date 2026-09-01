from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_current_user, get_db
from app.models import User
from app.security import hash_password
from app.schemas import UserCreate, UserResponse


router = APIRouter()


@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(
        User.username == user.username).first()

    if existing_user is not None:
        raise HTTPException(status_code=409, detail="Username already exists")

    new_user = User(username=user.username,
                    hashed_password=hash_password(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
