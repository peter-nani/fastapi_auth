# auth/exports.py

# Internal relative imports to maintain portability across different apps
from .auth_main import auth_router
from .dependencies import (
    get_current_active_user, 
    get_current_user, 
    get_optional_user
)
from .db import get_session, engine
from .models import Base, User
from .schema import (
    UserCreate, 
    UserResponse, 
    Token, 
    UserBase, 
    UserLogin
)
from .config import auth_settings

# Defining __all__ ensures clean imports when using 'from auth.exports import *'
__all__ = [
    "auth_router",
    "get_current_active_user",
    "get_current_user",
    "get_optional_user",
    "get_session",
    "engine",
    "Base",
    "User",
    "UserCreate",
    "UserResponse",
    "UserBase",
    "UserLogin",
    "Token",
    "auth_settings"
]