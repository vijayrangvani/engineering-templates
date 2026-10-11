"""PRACTICE: router for /items.
Reference answer: ../../../../fastapi-app/app/routers/items.py

Shape: router = APIRouter(prefix="/items", tags=["items"])
  GET    ""            -> list (cap limit at 100)
  GET    "/{item_id}"  -> 404 if missing
  POST   ""            -> 201
  PATCH  "/{item_id}"  -> 404 if missing
  DELETE "/{item_id}"  -> 204, 404 if missing
Every route takes `db: DbSession` (put it BEFORE params that have defaults).
"""
# TODO
