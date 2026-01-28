from typing import Annotated, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

# Internal relative imports
from .db import get_session
from . import models
from .config import auth_settings

# Standardized token URL based on the auth_router prefix we set earlier
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=auth_settings.TOKEN_URL, 
    auto_error=False  # Allows us to handle optional auth manually
)

async def get_current_user(
    token: Annotated[Optional[str], Depends(oauth2_scheme)] = None,
    session: Session = Depends(get_session)
) -> Optional[models.User]:
    """
    Decodes the JWT to find the user. Returns None if no token is provided.
    """
    if not token:
        return None
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Pulling keys directly from our centralized auth_settings
        payload = jwt.decode(
            token, 
            auth_settings.SECRET_KEY, 
            algorithms=[auth_settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = session.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise credentials_exception
        
    return user

async def get_current_active_user(
    current_user: Annotated[Optional[models.User], Depends(get_current_user)] = None
) -> models.User:
    """
    Ensures the user is logged in AND their account is active.
    """
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )
    
    # Check both the 'disabled' and 'is_active' flags from your models.py
    if current_user.disabled or not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive or disabled user"
        )
    
    return current_user

async def get_optional_user(
    current_user: Annotated[Optional[models.User], Depends(get_current_user)] = None
):
    """
    Helper for routes that can be accessed as a guest or a logged-in user.
    """
    return current_user