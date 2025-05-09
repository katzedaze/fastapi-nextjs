from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.order import Order, OrderCreate, OrderUpdate
from app.services.order import OrderService

router = APIRouter()


@router.get("", response_model=List[Order])
async def read_orders(
    skip: int = 0,
    limit: int = 100,
    user_id: Optional[UUID] = Query(
        None, description="Filter orders by user ID"),
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve orders.
    """
    if user_id:
        orders = await OrderService.get_by_user_id(db, user_id=user_id, skip=skip, limit=limit)
    else:
        orders = await OrderService.get_all(db, skip=skip, limit=limit)
    return orders


@router.post("", response_model=Order, status_code=status.HTTP_201_CREATED)
async def create_order(
    order_in: OrderCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create new order.
    """
    order = await OrderService.create(db, obj_in=order_in)
    return order


@router.get("/{order_id}", response_model=Order)
async def read_order(
    order_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific order by id.
    """
    order = await OrderService.get_by_id(db, order_id=order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
    return order


@router.put("/{order_id}", response_model=Order)
async def update_order(
    order_id: UUID,
    order_in: OrderUpdate,
    db: AsyncSession = Depends(get_db),
):
    """
    Update an order.
    """
    order = await OrderService.get_by_id(db, order_id=order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
    order = await OrderService.update(db, db_obj=order, obj_in=order_in)
    return order


@router.delete("/{order_id}", response_model=Order)
async def delete_order(
    order_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """
    Delete an order.
    """
    order = await OrderService.get_by_id(db, order_id=order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
    order = await OrderService.delete(db, db_obj=order)
    return order
