from typing import List, Optional
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate


class ItemService:
    """Service for Item related operations."""

    @staticmethod
    async def get_by_id(db: AsyncSession, item_id: UUID) -> Optional[Item]:
        """Get an item by ID."""
        result = await db.execute(select(Item).where(Item.id == item_id))
        return result.scalars().first()

    @staticmethod
    async def get_by_name(db: AsyncSession, name: str) -> Optional[Item]:
        """Get an item by name."""
        result = await db.execute(select(Item).where(Item.name == name))
        return result.scalars().first()

    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Item]:
        """Get all items."""
        result = await db.execute(select(Item).offset(skip).limit(limit))
        return result.scalars().all()

    @staticmethod
    async def create(db: AsyncSession, obj_in: ItemCreate) -> Item:
        """Create a new item."""
        db_obj = Item(
            name=obj_in.name,
            description=obj_in.description,
            price=obj_in.price,
            stock=obj_in.stock,
            image_url=obj_in.image_url,
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    @staticmethod
    async def update(
        db: AsyncSession, db_obj: Item, obj_in: ItemUpdate
    ) -> Item:
        """Update an item."""
        update_data = obj_in.dict(exclude_unset=True)

        # Update attributes
        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    @staticmethod
    async def delete(db: AsyncSession, db_obj: Item) -> Item:
        """Delete an item."""
        await db.delete(db_obj)
        await db.commit()
        return db_obj
