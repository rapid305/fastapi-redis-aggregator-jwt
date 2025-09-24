from datetime import datetime, timedelta, timezone
from typing import Annotated
import os
import logging

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dotenv import load_dotenv

from api.db.db_postgres import get_session
from api.auth.auth_schemes import TokenData
from api.auth.auth_model import User

load_dotenv(override=True)

# ------------------------------------------------------------------------------
# Settings for JWT

SECRET_KEY = os.getenv("SECRET_KEY_FOR_JWT")  # Secret key from .env file for JWT
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY_FOR_JWT not set")
ALGORITHM = "HS256"  # Algorithm used for encoding the JWT
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token expiration time in minutes


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")  # scheme for OAuth2

pwd_context = CryptContext(
    schemes=["bcrypt"], deprecated="auto"
)  # Password hashing context

# ------------------------------------------------------------------------------


# Hashing the password
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# Verifying the password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# Creating JWT token
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Fetching user from DB
async def get_user_from_db(session: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    res = await session.execute(stmt)
    return res.scalars().first()


# Getting current user from token
async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(get_session),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = await get_user_from_db(session, token_data.username)
    if user is None:
        raise credentials_exception
    return user


# Ensuring the user is active
async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    # Используем поле is_active из модели
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
