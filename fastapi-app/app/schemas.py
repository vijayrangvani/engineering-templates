"""TEMPLATE: Pydantic schemas = API contract (what comes IN, what goes OUT).

Keep them separate from ORM models: the API shape and the table shape evolve independently.
"""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ItemBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = None
    price: float = Field(gt=0)            # validation -> bad input returns 422 automatically


class ItemCreate(ItemBase):               # POST body
    pass


class ItemUpdate(BaseModel):              # PATCH body: every field optional
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = None
    price: float | None = Field(default=None, gt=0)


class ItemOut(ItemBase):                  # response body
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)   # allow building from an ORM object
