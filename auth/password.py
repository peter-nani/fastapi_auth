from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext

# Use relative import to ensure it works when the 'auth' folder is moved
from .config import auth_settings

# Initialize the password hashing context
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain text password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hashes a password using the configured bcrypt algorithm."""
    return pwd_context.hash(password)

# Token creation
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Creates a signed JWT access token using settings from config.py."""
    to_encode = data.copy()
    
    # Use the expiration from settings if no specific delta is provided
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=auth_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    to_encode.update({"exp": expire})
    
    # Critical Fix: Pull SECRET_KEY and ALGORITHM from auth_settings
    encoded_jwt = jwt.encode(
        to_encode, 
        auth_settings.SECRET_KEY, 
        algorithm=auth_settings.ALGORITHM
    )
    return encoded_jwt

# Token verification
def verify_token(token: str) -> Optional[dict]:
    """Decodes and validates a JWT token."""
    try:
        payload = jwt.decode(
            token, 
            auth_settings.SECRET_KEY, 
            algorithms=[auth_settings.ALGORITHM]
        )
        return payload
    except JWTError:
        return None