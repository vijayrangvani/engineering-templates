"""PRACTICE: data-access functions (only this file touches the DB).
Reference answer: ../../../fastapi-app/app/crud.py

Functions to write:
  list_items(db, skip, limit)   -> select(...).offset().limit(), db.scalars
  get_item(db, item_id)         -> db.get
  create_item(db, data)         -> add -> flush -> refresh -> return
  update_item(db, item, data)   -> model_dump(exclude_unset=True) -> setattr -> flush
  delete_item(db, item)         -> db.delete
"""
# TODO
