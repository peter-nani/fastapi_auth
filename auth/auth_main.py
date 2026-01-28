from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

# Use relative imports so the module is portable
from .models import *
from .db import *
from .schema import *
from .password import (
    get_password_hash, 
    verify_password, 
    create_access_token,
)
from .dependencies import get_current_active_user
from .config import auth_settings
# Create API Router for auth routes
# We remove 'app = FastAPI()' so this doesn't conflict with the main app
auth_router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
    responses={404: {"description": "Not found"}},
)

# --- AUTH ROUTES ---

@auth_router.post("/register", response_model=UserResponse)
def register_user(
    user: UserCreate,
    session: Session = Depends(get_session)
):
    db_user = session.query(User).filter(
        (User.email == user.email) | 
        (User.username == user.username)
    ).first()
    
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email or username already registered"
        )
    
    hashed_password = get_password_hash(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password
    )
    
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

@auth_router.post("/login", response_model=Token)
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(get_session)
):
    db_user = session.query(User).filter(User.username == form_data.username).first()
    
    if not db_user or not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(
        data={"sub": db_user.username, "user_id": db_user.id, "email": db_user.email},
        expires_delta=timedelta(minutes=auth_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}

# --- PROTECTED USER ROUTES ---
# We attach these to the router, so they are part of the 'auth' package

@auth_router.get("/me", response_model=UserResponse)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user

@auth_router.get("/health")
async def health_check():
    return {"status": "auth-module-active"}