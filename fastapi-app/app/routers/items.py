"""TEMPLATE: router = one resource's endpoints. Thin: validate -> call crud -> return."""
from fastapi import APIRouter, HTTPException, status

from app import crud, schemas
from app.db import DbSession

router = APIRouter(prefix="/items", tags=["items"])


@router.get("", response_model=list[schemas.ItemOut])
def list_items(skip: int = 0, limit: int = 20, db: DbSession):
    return crud.list_items(db, skip, min(limit, 100))   # cap page size


@router.get("/{item_id}", response_model=schemas.ItemOut)
def get_item(item_id: int, db: DbSession):
    item = crud.get_item(db, item_id)
    if not item:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Item not found")
    return item


@router.post("", response_model=schemas.ItemOut, status_code=status.HTTP_201_CREATED)
def create_item(data: schemas.ItemCreate, db: DbSession):
    return crud.create_item(db, data)


@router.patch("/{item_id}", response_model=schemas.ItemOut)
def update_item(item_id: int, data: schemas.ItemUpdate, db: DbSession):
    item = crud.get_item(db, item_id)
    if not item:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Item not found")
    return crud.update_item(db, item, data)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, db: DbSession):
    item = crud.get_item(db, item_id)
    if not item:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Item not found")
    crud.delete_item(db, item)
