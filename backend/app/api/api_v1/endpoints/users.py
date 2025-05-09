from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.user import User, UserCreate, UserUpdate
from app.services.user import UserService

router = APIRouter()


@router.get("", response_model=List[User])
async def read_users(
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve users.
    """
    users = await UserService.get_all(db, skip=skip, limit=limit)
    return users


@router.post("", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: UserCreate, 
    db: AsyncSession = Depends(get_db)
):
    """
    Create new user.
    """
    user = await UserService.create(db, obj_in=user_in)
    return user


@router.get("/{user_id}", response_model=User)
async def read_user(
    user_id: UUID, 
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific user by id.
    """
    user = await UserService.get_by_id(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


@router.put("/{user_id}", response_model=User)
async def update_user(
    user_id: UUID,
    user_in: UserUpdate,
    db: AsyncSession = Depends(get_db),
):
    """
    Update a user.
    """
    user = await UserService.get_by_id(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    user = await UserService.update(db, db_obj=user, obj_in=user_in)
    return user


@router.delete("/{user_id}", response_model=User)
async def delete_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """
    Delete a user.
    """
    user = await UserService.get_by_id(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    user = await UserService.delete(db, db_obj=user)
    return user