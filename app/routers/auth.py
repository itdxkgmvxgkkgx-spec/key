from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..config import settings
from ..database import get_db
from ..deps import get_current_user
from ..models import User
from ..security import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/api/auth", tags=["auth"])


class RegisterIn(BaseModel):
    username: str = Field(min_length=3, max_length=32, pattern=r"^[a-zA-Z0-9_.-]+$")
    password: str = Field(min_length=6, max_length=128)
    email: str | None = Field(default=None, max_length=255)


class LoginIn(BaseModel):
    username: str
    password: str


def user_public(u: User) -> dict:
    return {
        "id": u.id,
        "username": u.username,
        "email": u.email,
        "is_admin": u.is_admin,
        "is_active": u.is_active,
        "daily_quota": u.daily_quota,
        "created_at": u.created_at.isoformat() if u.created_at else None,
    }


@router.post("/register", status_code=201)
async def register(body: RegisterIn, db: AsyncSession = Depends(get_db)):
    if not settings.REGISTRATION_OPEN:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="registration_closed")
    exists = await db.execute(select(User).where(User.username == body.username))
    if exists.scalar_one_or_none():
        raise HTTPException(status.HTTP_409_CONFLICT, detail="username_taken")
    user = User(
        username=body.username,
        email=body.email,
        password_hash=hash_password(body.password),
        daily_quota=settings.DEFAULT_DAILY_QUOTA,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return {"token": create_access_token(user.id), "user": user_public(user)}


@router.post("/login")
async def login(body: LoginIn, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(User).where(User.username == body.username))
    user = res.scalar_one_or_none()
    if not user or not verify_password(body.password, user.password_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="invalid_credentials")
    if not user.is_active:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="user_suspended")
    return {"token": create_access_token(user.id), "user": user_public(user)}


@router.get("/me")
async def me(user: User = Depends(get_current_user)):
    return user_public(user)
