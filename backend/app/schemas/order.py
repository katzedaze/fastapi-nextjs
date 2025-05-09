from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.order import OrderStatus


class OrderItemBase(BaseModel):
    """Base schema for OrderItem data (中間テーブル)."""
    item_id: UUID
    quantity: int = Field(..., gt=0)
    price_at_time: float = Field(..., gt=0)


class OrderItemCreate(OrderItemBase):
    """Schema for creating a new order item."""
    pass


class OrderBase(BaseModel):
    """Base schema for Order data."""
    user_id: UUID
    status: OrderStatus = OrderStatus.PENDING
    shipping_address: Optional[str] = None
    total_amount: float = Field(..., gt=0)
    notes: Optional[str] = None


class OrderCreate(OrderBase):
    """Schema for creating a new order."""
    items: List[OrderItemCreate]


class OrderUpdate(BaseModel):
    """Schema for updating an order."""
    status: Optional[OrderStatus] = None
    shipping_address: Optional[str] = None
    notes: Optional[str] = None


# Import Item schema to use in response
from app.schemas.item import Item as ItemSchema


class OrderItem(OrderItemBase):
    """Schema for OrderItem data."""
    order_id: UUID
    item: Optional[ItemSchema] = None

    class Config:
        from_attributes = True


class OrderInDBBase(OrderBase):
    """Base schema for Order data in the database."""
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Order(OrderInDBBase):
    """Schema for Order data with items."""
    items: List[ItemSchema] = []

    class Config:
        from_attributes = True