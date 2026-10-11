"""PRACTICE: Pydantic schemas (API contract).
Reference answer: ../../../fastapi-app/app/schemas.py

Shape:
  ItemBase   : name (1-100 chars), description optional, price > 0
  ItemCreate : same as base
  ItemUpdate : every field optional (for PATCH)
  ItemOut    : base + id + created_at, model_config from_attributes=True
"""
# TODO
