from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..deps import get_current_user
from ..models import User
from ..services import quota

router = APIRouter(prefix="/api/me", tags=["dashboard"])


@router.get("/stats")
async def my_stats(user: User = Depends(get_current_user),
                   db: AsyncSession = Depends(get_db)):
    used_today = await quota.get_today_usage(db, user.id)
    total = await quota.total_requests(db, user.id)
    history = await quota.last_7_days(db, user.id)
    return {
        "username": user.username,
        "daily_quota": user.daily_quota,
        "used_today": used_today,
        "remaining_today": max(0, user.daily_quota - used_today),
        "total_requests": total,
        "history_7d": history,
    }
