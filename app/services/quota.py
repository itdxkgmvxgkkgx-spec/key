"""Daily quota accounting. One row per user per UTC day, auto-renewing."""
import time
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import APIKey, DailyUsage, UsageLog, User


def today_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


async def get_today_usage(db: AsyncSession, user_id: int) -> int:
    res = await db.execute(
        select(DailyUsage.count).where(
            DailyUsage.user_id == user_id, DailyUsage.date == today_utc()
        )
    )
    return res.scalar_one_or_none() or 0


async def consume_quota(db: AsyncSession, user: User) -> tuple[int, int]:
    """Consume 1 request. Returns (used_today, daily_quota). Raises 429 if exceeded."""
    date = today_utc()
    res = await db.execute(
        select(DailyUsage).where(DailyUsage.user_id == user.id, DailyUsage.date == date)
    )
    row = res.scalar_one_or_none()
    if row is None:
        row = DailyUsage(user_id=user.id, date=date, count=0)
        db.add(row)
        await db.flush()
    if row.count >= user.daily_quota:
        raise HTTPException(
            status.HTTP_429_TOO_MANY_REQUESTS,
            detail={"error": "quota_exceeded", "used": row.count, "quota": user.daily_quota},
        )
    row.count += 1
    return row.count, user.daily_quota


async def log_request(db: AsyncSession, user: User, api_key: APIKey,
                      endpoint: str, query: str, status_code: int,
                      started: float):
    api_key.total_requests += 1
    api_key.last_used_at = datetime.now(timezone.utc)
    db.add(UsageLog(
        user_id=user.id,
        endpoint=endpoint,
        query=query[:500],
        status=status_code,
        response_ms=round((time.perf_counter() - started) * 1000, 2),
    ))


async def total_requests(db: AsyncSession, user_id: int) -> int:
    res = await db.execute(
        select(func.coalesce(func.sum(APIKey.total_requests), 0)).where(
            APIKey.user_id == user_id
        )
    )
    return int(res.scalar_one())


async def last_7_days(db: AsyncSession, user_id: int) -> list[dict]:
    res = await db.execute(
        select(DailyUsage.date, DailyUsage.count)
        .where(DailyUsage.user_id == user_id)
        .order_by(DailyUsage.date.desc())
        .limit(7)
    )
    return [{"date": d, "count": c} for d, c in res.all()][::-1]
