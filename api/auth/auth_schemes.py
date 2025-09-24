from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# Pydantic models for user creation, output, and token data
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=30)
    email: EmailStr
    password: str = Field(..., min_length=6)
    full_name: Optional[str] = None


# Pydantic model for user output (excluding sensitive information)
class UserOut(BaseModel):
    id: str
    username: str
    email: str
    full_name: Optional[str] = None
    is_active: bool
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Pydantic model for token data
class TokenData(BaseModel):
    username: str | None = None


# Pydantic model for JWT token response
class Token(BaseModel):
    access_token: str
    token_type: str
