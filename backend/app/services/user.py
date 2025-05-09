from typing import List, Optional
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    """Service for User related operations."""

    @staticmethod
    async def get_by_id(db: AsyncSession, user_id: UUID) -> Optional[User]:
        """Get a user by ID."""
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalars().first()

    @staticmethod
    async def get_by_email(db: AsyncSession, email: str) -> Optional[User]:
        """Get a user by email."""
        result = await db.execute(select(User).where(User.email == email))
        return result.scalars().first()

    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users."""
        result = await db.execute(select(User).offset(skip).limit(limit))
        return result.scalars().all()

    @staticmethod
    async def create(db: AsyncSession, obj_in: UserCreate) -> User:
        """Create a new user."""
        # Check if user with this email already exists
        existing_user = await UserService.get_by_email(db, email=obj_in.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        # Create new user
        hashed_password = get_password_hash(obj_in.password)
        db_obj = User(
            email=obj_in.email,
            hashed_password=hashed_password,
            full_name=obj_in.full_name,
            is_active=obj_in.is_active,
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    @staticmethod
    async def update(
        db: AsyncSession, db_obj: User, obj_in: UserUpdate
    ) -> User:
        """Update a user."""
        update_data = obj_in.dict(exclude_unset=True)
        
        if "password" in update_data:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password

        # Update attributes
        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    @staticmethod
    async def delete(db: AsyncSession, db_obj: User) -> User:
        """Delete a user."""
        await db.delete(db_obj)
        await db.commit()
        return db_obj

    @staticmethod
    def authenticate(db_obj: User, password: str) -> bool:
        """Verify if password is correct."""
        if not db_obj:
            return False
        if not verify_password(password, db_obj.hashed_password):
            return False
        return True