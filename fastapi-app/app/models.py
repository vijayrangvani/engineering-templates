"""TEMPLATE: ORM model = one table. SQLAlchemy 2.0 typed style (Mapped + mapped_column)."""
from datetime import datetime

from sqlalchemy import Float, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True)                 # auto-increment PK
    name: Mapped[str] = mapped_column(String(100), index=True)       # index = fast lookups by name
    description: Mapped[str | None] = mapped_column(String(500))     # `| None` -> nullable column
    # Explicit type: SQLAlchemy's default for `float` changed (Float -> Double) between versions,
    # which made `alembic check` report a drift. For real money, prefer Numeric(10, 2) + Decimal.
    price: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())  # DB fills the time
