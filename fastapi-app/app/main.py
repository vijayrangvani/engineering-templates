"""TEMPLATE: app entry point. Wires settings, DB tables, middleware, routers, health checks.

Run:  uvicorn app.main:app --reload
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.config import settings
from app.db import Base, SessionLocal, engine
from app.routers import items


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create tables if missing. Fine for learning; real projects use Alembic migrations.
    Base.metadata.create_all(bind=engine)
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
def ready():
    with SessionLocal() as db:
        db.execute(text("SELECT 1"))
    return {"status": "ready"}
