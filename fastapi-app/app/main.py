"""TEMPLATE: app entry point. Wires settings, DB tables, middleware, routers, health checks.

Run:  uvicorn app.main:app --reload
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text

from app.config import settings
from app.db import DbSession, engine
from app.routers import items

log = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # No `Base.metadata.create_all()` here: Alembic owns the schema. create_all would make the
    # tables WITHOUT Alembic's version table, and the next `alembic upgrade head` would then fail
    # with "table already exists". Run `alembic upgrade head` before starting (see MIGRATIONS.md).
    yield
    # Shutdown: release pooled connections.
    engine.dispose()


app = FastAPI(title=settings.app_name, lifespan=lifespan)

# CORS: only matters for browsers calling from another origin. List origins explicitly in prod.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(items.router)


@app.get("/health")            # liveness: "process is alive" (no dependencies)
def health():
    return {"status": "ok"}


@app.get("/ready")             # readiness: "can serve traffic" (checks the DB)
def ready(db: DbSession):
    try:
        db.execute(text("SELECT 1"))   # fails fast: the engine sets a connect timeout (app/db.py)
    except Exception as e:  # noqa: BLE001  any DB failure means "not ready"
        log.warning("readiness check failed: %s", e)
        # 503 = "skip this pod for now"; an unhandled error would be a 500 with a stack trace.
        return JSONResponse(status_code=503, content={"status": "not ready"})
    return {"status": "ready"}
