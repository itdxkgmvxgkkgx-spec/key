from fastapi import Depends, Header, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .database import get_db
from .models import APIKey, User
from .security import decode_access_token


def _extract_bearer(authorization: str | None) -> str | None:
    if authorization and authorization.lower().startswith("bearer "):
        return authorization[7:].strip()
    return None


async def get_current_user(
    authorization: str | None = Header(default=None),
    db: AsyncSession = Depends(get_db),
) -> User:
    """Dashboard session auth via JWT (Authorization: Bearer <jwt>)."""
    token = _extract_bearer(authorization)
    if not token:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="missing_token")
    user_id = decode_access_token(token)
    if user_id is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="invalid_token")
    user = await db.get(User, user_id)
    if not user or not user.is_active:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="user_inactive")
    return user


async def require_admin(user: User = Depends(get_current_user)) -> User:
    if not user.is_admin:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="admin_only")
    return user


async def get_user_by_api_key(
    x_api_key: str | None = Header(default=None),
    authorization: str | None = Header(default=None),
    db: AsyncSession = Depends(get_db),
) -> tuple[User, APIKey]:
    """Programmatic API auth via X-API-Key header or Bearer nvsk_... key."""
    raw = x_api_key or _extract_bearer(authorization)
    if not raw:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="missing_api_key")
    res = await db.execute(select(APIKey).where(APIKey.key == raw))
    api_key = res.scalar_one_or_none()
    if not api_key or not api_key.is_active:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="invalid_api_key")
    user = await db.get(User, api_key.user_id)
    if not user or not user.is_active:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="user_suspended")
    return user, api_key
