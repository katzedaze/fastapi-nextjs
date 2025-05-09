from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class ItemBase(BaseModel):
    """Base schema for Item data."""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)
    image_url: Optional[str] = None


class ItemCreate(ItemBase):
    """Schema for creating a new item."""
    pass


class ItemUpdate(BaseModel):
    """Schema for updating an item."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    image_url: Optional[str] = None


class ItemInDBBase(ItemBase):
    """Base schema for Item data in the database."""
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Item(ItemInDBBase):
    """Schema for Item data."""
    pass