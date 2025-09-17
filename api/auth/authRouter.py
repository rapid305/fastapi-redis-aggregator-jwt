from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm

from api.db.db_postgres import get_session
from api.auth.auth_model import User  # SQLAlchemy модель
from api.auth.auth_schemes import Token, UserCreate, UserOut
from api.auth.auth_service import create_access_token, verify_password, get_password_hash

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session)
):
    stmt = select(User).where(User.username == form_data.username)
    result = await session.execute(stmt)
    user = result.scalars().first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=UserOut, status_code=201)
async def register(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_session)
):
    # Проверка уникальности
    existing = await session.execute(
        select(User).where(
            (User.username == user_data.username) | (User.email == user_data.email)
        )
    )
    if existing.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists"
        )

    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hashed_password,
        is_active=True
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user


@router.get("/get-user")
async def get_user():
    return {"message": "Get user endpoint"}


@router.get("/get-user/{user_id}/details")
async def get_user_from_db(user_id: str, session: AsyncSession = Depends(get_session)):
    stmt = select(User).where(User.id == user_id)
    res = await session.execute(stmt)
    user = res.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserOut.model_validate(user)
