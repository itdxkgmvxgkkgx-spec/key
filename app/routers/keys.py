from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..deps import get_current_user
from ..models import APIKey, User
from ..security import generate_api_key

router = APIRouter(prefix="/api/keys", tags=["api-keys"])

MAX_KEYS_PER_USER = 10


class KeyCreateIn(BaseModel):
    name: str = Field(default="default", min_length=1, max_length=64)


def key_public(k: APIKey, reveal: bool = False) -> dict:
    return {
        "id": k.id,
        "name": k.name,
        "key": k.key if reveal else k.key[:12] + "…" + k.key[-4:],
        "is_active": k.is_active,
        "total_requests": k.total_requests,
        "created_at": k.created_at.isoformat() if k.created_at else None,
        "last_used_at": k.last_used_at.isoformat() if k.last_used_at else None,
    }


@router.get("")
async def list_keys(user: User = Depends(get_current_user),
                    db: AsyncSession = Depends(get_db)):
    res = await db.execute(
        select(APIKey).where(APIKey.user_id == user.id).order_by(APIKey.id.desc())
    )
    return {"keys": [key_public(k, reveal=True) for k in res.scalars().all()]}


@router.post("", status_code=201)
async def create_key(body: KeyCreateIn, user: User = Depends(get_current_user),
                     db: AsyncSession = Depends(get_db)):
    res = await db.execute(
        select(APIKey).where(APIKey.user_id == user.id, APIKey.is_active == True)  # noqa: E712
    )
    if len(res.scalars().all()) >= MAX_KEYS_PER_USER:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="max_keys_reached")
    key = APIKey(key=generate_api_key(), name=body.name, user_id=user.id)
    db.add(key)
    await db.commit()
    await db.refresh(key)
    return key_public(key, reveal=True)


@router.delete("/{key_id}")
async def revoke_key(key_id: int, user: User = Depends(get_current_user),
                     db: AsyncSession = Depends(get_db)):
    key = await db.get(APIKey, key_id)
    if not key or (key.user_id != user.id and not user.is_admin):
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="key_not_found")
    key.is_active = False
    await db.commit()
    return {"revoked": True}
