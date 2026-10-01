import asyncio
import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select

from .config import settings
from .database import async_session, engine
from .models import APIKey, Base, User
from .routers import admin, auth, dashboard, keys, search
from .security import generate_api_key, hash_password
from .services.search import warmup

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(name)s %(message)s")
log = logging.getLogger("novaseek")

STATIC_DIR = Path(__file__).resolve().parent.parent / "static"


async def ensure_owner():
    """Create/refresh the owner account from env (GitHub Secrets) + default key."""
    async with async_session() as db:
        res = await db.execute(select(User).where(User.username == settings.OWNER_USERNAME))
        owner = res.scalar_one_or_none()
        if owner is None:
            owner = User(
                username=settings.OWNER_USERNAME,
                password_hash=hash_password(settings.OWNER_PASSWORD),
                is_admin=True,
                daily_quota=1_000_000,
            )
            db.add(owner)
            await db.flush()
            db.add(APIKey(key=generate_api_key(), name="owner-master", user_id=owner.id))
            log.info("Owner account '%s' created", settings.OWNER_USERNAME)
        else:
            owner.is_admin = True
            owner.password_hash = hash_password(settings.OWNER_PASSWORD)
        await db.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await ensure_owner()
    asyncio.create_task(warmup())
    log.info("%s is ready", settings.APP_NAME)
    yield
    await engine.dispose()


app = FastAPI(
    title="NovaSeek Search API",
    version="1.0.0",
    description="Blazing-fast, self-hosted, unlimited search API with API keys, "
                "daily quotas and a bilingual dashboard.",
    lifespan=lifespan,
)

app.add_middleware(GZipMiddleware, minimum_size=1024)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(keys.router)
app.include_router(search.router)
app.include_router(dashboard.router)
app.include_router(admin.router)


@app.get("/api/health", tags=["meta"])
async def health():
    return {"status": "ok", "service": settings.APP_NAME, "version": "1.0.0"}


@app.get("/", include_in_schema=False)
async def index():
    return FileResponse(STATIC_DIR / "index.html")


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
