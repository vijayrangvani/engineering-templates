"""TEMPLATE: async endpoints + background jobs.

Pattern: POST creates a job row (status=pending) and returns 202 immediately ->
background task does the slow work and updates the row -> client polls GET /reports/{id}.

BackgroundTasks runs in the same process after the response: fine for short jobs (emails, small
LLM calls). For long / must-not-lose jobs use a real queue: Celery or arq + Redis, separate worker.
"""
import asyncio
from contextlib import asynccontextmanager

from fastapi import BackgroundTasks, FastAPI, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base, DbSession, SessionLocal, engine


class Report(Base):
    __tablename__ = "reports"
    id: Mapped[int] = mapped_column(primary_key=True)
    topic: Mapped[str] = mapped_column(String(200))
    status: Mapped[str] = mapped_column(String(20), default="pending")   # pending -> done / failed
    result: Mapped[str | None]


class ReportIn(BaseModel):
    topic: str


class ReportOut(BaseModel):
    id: int
    topic: str
    status: str
    result: str | None
    model_config = ConfigDict(from_attributes=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)   # create_all is sync -> run_sync bridge
    yield
    await engine.dispose()


app = FastAPI(title="async-jobs", lifespan=lifespan)


async def generate_report(report_id: int) -> None:
    """Runs AFTER the response is sent. The request's session is closed by now, so open a NEW one."""
    async with SessionLocal() as db:
        report = await db.get(Report, report_id)
        try:
            await asyncio.sleep(0.1)                     # stand-in for slow work (LLM call, PDF, ...)
            report.result = f"Report about {report.topic}"
            report.status = "done"
        except Exception:  # noqa: BLE001  deliberate: any failure must mark the job
            report.status = "failed"                     # never leave a job stuck in pending
        await db.commit()


@app.post("/reports", response_model=ReportOut, status_code=status.HTTP_202_ACCEPTED)
async def create_report(data: ReportIn, db: DbSession, background: BackgroundTasks):
    report = Report(topic=data.topic)
    db.add(report)
    await db.commit()          # commit NOW so the background task can see the row
    background.add_task(generate_report, report.id)
    return report


@app.get("/reports/{report_id}", response_model=ReportOut)
async def get_report(report_id: int, db: DbSession):
    report = await db.get(Report, report_id)
    if not report:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Report not found")
    return report


@app.get("/parallel")
async def parallel():
    """asyncio.gather: run independent awaits concurrently -> total time = slowest, not the sum."""
    async def call(name: str, seconds: float) -> str:
        await asyncio.sleep(seconds)     # e.g. 3 API calls
        return name
    return {"results": await asyncio.gather(call("a", 0.1), call("b", 0.1), call("c", 0.1))}
