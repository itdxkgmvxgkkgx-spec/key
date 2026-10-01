from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..deps import require_admin
from ..models import APIKey, DailyUsage, User
from ..services import quota

router = APIRouter(prefix="/api/admin", tags=["admin"])


class UserPatchIn(BaseModel):
    is_active: bool | None = None
    daily_quota: int | None = Field(default=None, ge=0, le=10_000_000)


def admin_user_view(u: User, used_today: int, total: int) -> dict:
    return {
        "id": u.id,
        "username": u.username,
        "email": u.email,
        "is_admin": u.is_admin,
        "is_active": u.is_active,
        "daily_quota": u.daily_quota,
        "used_today": used_today,
        "total_requests": total,
        "created_at": u.created_at.isoformat() if u.created_at else None,
    }


@router.get("/overview")
async def overview(admin: User = Depends(require_admin),
                   db: AsyncSession = Depends(get_db)):
    users = (await db.execute(select(func.count(User.id)))).scalar_one()
    keys = (await db.execute(
        select(func.count(APIKey.id)).where(APIKey.is_active == True)  # noqa: E712
    )).scalar_one()
    today = quota.today_utc()
    req_today = (await db.execute(
        select(func.coalesce(func.sum(DailyUsage.count), 0)).where(DailyUsage.date == today)
    )).scalar_one()
    return {"users": users, "active_api_keys": keys, "requests_today": int(req_today)}


@router.get("/users")
async def list_users(admin: User = Depends(require_admin),
                     db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(User).order_by(User.id))
    out = []
    for u in res.scalars().all():
        used = await quota.get_today_usage(db, u.id)
        total = await quota.total_requests(db, u.id)
        out.append(admin_user_view(u, used, total))
    return {"users": out}


@router.patch("/users/{user_id}")
async def patch_user(user_id: int, body: UserPatchIn,
                     admin: User = Depends(require_admin),
                     db: AsyncSession = Depends(get_db)):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="user_not_found")
    if user.id == admin.id and body.is_active is False:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="cannot_suspend_self")
    if body.is_active is not None:
        user.is_active = body.is_active
    if body.daily_quota is not None:
        user.daily_quota = body.daily_quota
    await db.commit()
    used = await quota.get_today_usage(db, user.id)
    total = await quota.total_requests(db, user.id)
    return admin_user_view(user, used, total)


@router.get("/users/{user_id}/usage")
async def user_usage(user_id: int, admin: User = Depends(require_admin),
                     db: AsyncSession = Depends(get_db)):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="user_not_found")
    keys = (await db.execute(
        select(APIKey).where(APIKey.user_id == user_id)
    )).scalars().all()
    return {
        "user": user.username,
        "used_today": await quota.get_today_usage(db, user_id),
        "daily_quota": user.daily_quota,
        "total_requests": await quota.total_requests(db, user_id),
        "history_7d": await quota.last_7_days(db, user_id),
        "keys": [{"name": k.name, "active": k.is_active,
                  "total_requests": k.total_requests,
                  "last_used_at": k.last_used_at.isoformat() if k.last_used_at else None}
                 for k in keys],
    }
