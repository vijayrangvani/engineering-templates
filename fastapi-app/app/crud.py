"""TEMPLATE: data-access layer. Routes call these; only this file talks SQL.

Why: routes stay thin, and you can test / swap the DB logic in one place.
"""
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas


def list_items(db: Session, skip: int = 0, limit: int = 20) -> list[models.Item]:
    stmt = select(models.Item).offset(skip).limit(limit)   # 2.0 style: build a statement...
    return list(db.scalars(stmt))                          # ...then execute -> ORM objects


def get_item(db: Session, item_id: int) -> models.Item | None:
    return db.get(models.Item, item_id)                    # lookup by primary key


def create_item(db: Session, data: schemas.ItemCreate) -> models.Item:
    item = models.Item(**data.model_dump())
    db.add(item)
    db.flush()          # send INSERT now so item.id is filled; commit happens in get_db()
    db.refresh(item)    # reload server defaults (created_at)
    return item


def update_item(db: Session, item: models.Item, data: schemas.ItemUpdate) -> models.Item:
    for field, value in data.model_dump(exclude_unset=True).items():  # only fields the client sent
        setattr(item, field, value)
    db.flush()
    return item


def delete_item(db: Session, item: models.Item) -> None:
    db.delete(item)
