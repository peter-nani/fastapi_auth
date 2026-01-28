from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int] = None

# User schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(UserBase):
    id: int
    disabled: bool
    is_active: bool
    
    # Pydantic V2 way to handle SQLAlchemy objects
    model_config = ConfigDict(from_attributes=True)