"""TEMPLATE: async SQLAlchemy. Same shape as fastapi-app/app/db.py, with async versions of each piece.

sync -> async:  create_engine -> create_async_engine | sessionmaker -> async_sessionmaker
                db.commit() -> await db.commit()     | URL driver sqlite -> sqlite+aiosqlite
"""
import os
from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./app.db")

engine = create_async_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)  # False: objects usable after commit


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncIterator[AsyncSession]:
    async with SessionLocal() as db:           # `async with` closes the session for you
        try:
            yield db
            await db.commit()
        except Exception:
            await db.rollback()
            raise


DbSession = Annotated[AsyncSession, Depends(get_db)]
