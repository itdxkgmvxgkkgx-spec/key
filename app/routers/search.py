import time

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..deps import get_user_by_api_key
from ..models import APIKey, User
from ..services import quota
from ..services.search import search

router = APIRouter(prefix="/api/v1", tags=["search"])


@router.get("/search")
async def search_endpoint(
    q: str = Query(min_length=1, max_length=500, description="Search query"),
    lang: str = Query(default="auto", max_length=16,
                      description="Result language, e.g. fa, en, all, auto"),
    site: str | None = Query(default=None, max_length=255,
                             description="Restrict results to one site, e.g. wikipedia.org"),
    count: int = Query(default=10, ge=1, le=50),
    creds: tuple[User, APIKey] = Depends(get_user_by_api_key),
    db: AsyncSession = Depends(get_db),
):
    """Main search endpoint. Authenticate with `X-API-Key: nvsk_...`."""
    user, api_key = creds
    started = time.perf_counter()
    used, daily_quota = await quota.consume_quota(db, user)

    status_code = 200
    try:
        payload = await search(q, lang=lang, site=site, count=count)
    except ValueError:
        status_code = 400
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="empty_query")
    except Exception:
        status_code = 502
        raise HTTPException(status.HTTP_502_BAD_GATEWAY, detail="search_unavailable")
    finally:
        await quota.log_request(db, user, api_key, "search", q, status_code, started)
        await db.commit()

    payload["usage"] = {"used_today": used, "daily_quota": daily_quota,
                        "remaining_today": daily_quota - used}
    return payload


@router.get("/usage")
async def api_usage(creds: tuple[User, APIKey] = Depends(get_user_by_api_key),
                    db: AsyncSession = Depends(get_db)):
    """Check your quota programmatically with the same API key."""
    user, _ = creds
    used = await quota.get_today_usage(db, user.id)
    return {
        "username": user.username,
        "used_today": used,
        "daily_quota": user.daily_quota,
        "remaining_today": max(0, user.daily_quota - used),
        "renews": "daily at 00:00 UTC",
    }
