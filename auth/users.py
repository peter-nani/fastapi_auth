# users.py
from fastapi import APIRouter, Depends
from auth.db import get_session
from sqlmodel import select
import auth.models as models
from auth.schema import *
from auth.hash_passcode import get_password_hash, verify_password
router = APIRouter()

@router.get("/users")
def read_users(session=Depends(get_session)):
    Users = session.exec(select(models.User)).all()
    return Users

@router.post("/users")
def create_user(user: models.User, session=Depends(get_session)):
    hash_password = get_password_hash(user.password)
    user.password = hash_password
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.post("/get-user")
def get_user(username: str, session=Depends(get_session)):
    db_user = session.exec(
        select(models.User).where(models.User.username == username)
    ).first()
    if not db_user:
        return {"error": "User not found"}
    return db_user