"""PRACTICE: ORM model.
Reference answer: ../../../fastapi-app/app/models.py

Shape: class Item(Base) -> __tablename__ = "items"
  id (primary key) | name (String 100, indexed) | description (nullable) | price (float)
  created_at (server_default=func.now())
Use Mapped[...] + mapped_column(...)
"""
# TODO
