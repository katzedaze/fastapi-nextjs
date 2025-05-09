from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.item import Item, ItemCreate, ItemUpdate
from app.services.item import ItemService

router = APIRouter()


@router.get("", response_model=List[Item])
async def read_items(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve items.
    """
    items = await ItemService.get_all(db, skip=skip, limit=limit)
    return items


@router.post("", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(
    item_in: ItemCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create new item.
    """
    item = await ItemService.create(db, obj_in=item_in)
    return item


@router.get("/{item_id}", response_model=Item)
async def read_item(
    item_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific item by id.
    """
    item = await ItemService.get_by_id(db, item_id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )
    return item


@router.put("/{item_id}", response_model=Item)
async def update_item(
    item_id: UUID,
    item_in: ItemUpdate,
    db: AsyncSession = Depends(get_db),
):
    """
    Update an item.
    """
    item = await ItemService.get_by_id(db, item_id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )
    item = await ItemService.update(db, db_obj=item, obj_in=item_in)
    return item


@router.delete("/{item_id}", response_model=Item)
async def delete_item(
    item_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """
    Delete an item.
    """
    item = await ItemService.get_by_id(db, item_id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )
    item = await ItemService.delete(db, db_obj=item)
    return item
