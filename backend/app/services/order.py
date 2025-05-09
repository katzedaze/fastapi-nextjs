from typing import List, Optional
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.item import Item
from app.models.user import User
from app.schemas.order import OrderCreate, OrderUpdate


class OrderService:
    """Service for Order related operations."""

    @staticmethod
    async def get_by_id(db: AsyncSession, order_id: UUID) -> Optional[Order]:
        """Get an order by ID."""
        result = await db.execute(
            select(Order)
            .options(selectinload(Order.order_items).selectinload(OrderItem.item))
            .where(Order.id == order_id)
        )
        return result.scalars().first()

    @staticmethod
    async def get_by_user_id(db: AsyncSession, user_id: UUID, skip: int = 0, limit: int = 100) -> List[Order]:
        """Get orders by user ID."""
        result = await db.execute(
            select(Order)
            .options(selectinload(Order.order_items).selectinload(OrderItem.item))
            .where(Order.user_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Order]:
        """Get all orders."""
        result = await db.execute(
            select(Order)
            .options(selectinload(Order.order_items).selectinload(OrderItem.item))
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    @staticmethod
    async def create(db: AsyncSession, obj_in: OrderCreate) -> Order:
        """Create a new order."""
        # Verify user exists
        user_query = await db.execute(select(User).where(User.id == obj_in.user_id))
        user = user_query.scalars().first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        # Create order
        db_obj = Order(
            user_id=obj_in.user_id,
            status=obj_in.status,
            shipping_address=obj_in.shipping_address,
            total_amount=obj_in.total_amount,
            notes=obj_in.notes,
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)

        # Add order items
        for item_data in obj_in.items:
            # Verify item exists
            item_query = await db.execute(select(Item).where(Item.id == item_data.item_id))
            item = item_query.scalars().first()
            if not item:
                # Rollback order creation if item doesn't exist
                await db.delete(db_obj)
                await db.commit()
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Item with ID {item_data.item_id} not found",
                )

            # Check stock availability
            if item.stock < item_data.quantity:
                # Rollback order creation if stock is insufficient
                await db.delete(db_obj)
                await db.commit()
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Insufficient stock for item {item.name}",
                )

            # Add to order_items
            order_item = OrderItem(
                order_id=db_obj.id,
                item_id=item_data.item_id,
                quantity=item_data.quantity,
                price_at_time=item_data.price_at_time or item.price,
            )
            db.add(order_item)

            # Update item stock
            item.stock -= item_data.quantity
            db.add(item)

        await db.commit()
        return await OrderService.get_by_id(db, db_obj.id)

    @staticmethod
    async def update(
        db: AsyncSession, db_obj: Order, obj_in: OrderUpdate
    ) -> Order:
        """Update an order."""
        update_data = obj_in.dict(exclude_unset=True)

        # Update attributes
        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    @staticmethod
    async def delete(db: AsyncSession, db_obj: Order) -> Order:
        """Delete an order."""
        await db.delete(db_obj)
        await db.commit()
        return db_obj
