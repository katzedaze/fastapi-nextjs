from datetime import datetime
from typing import Any, Dict
from zoneinfo import ZoneInfo

import factory
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base_class import Base

JST = ZoneInfo("Asia/Tokyo")


class BaseSQLAlchemyModelFactory(factory.Factory):
    """Base factory for SQLAlchemy models with async session support."""

    class Meta:
        abstract = True

    @classmethod
    def _create(cls, model_class: type[Base], *args: Any, **kwargs: Any) -> Base:
        """Create instance with Japanese timezone timestamps."""
        now = datetime.now(JST).replace(tzinfo=None)
        
        if "created_at" not in kwargs:
            kwargs["created_at"] = now
        if "updated_at" not in kwargs:
            kwargs["updated_at"] = now
            
        return model_class(*args, **kwargs)

    @classmethod
    async def create_async(
        cls, db: AsyncSession, **kwargs: Any
    ) -> Base:
        """Create and save instance to database asynchronously."""
        instance = cls.build(**kwargs)
        db.add(instance)
        await db.commit()
        await db.refresh(instance)
        return instance

    @classmethod
    async def create_batch_async(
        cls, db: AsyncSession, size: int, **kwargs: Any
    ) -> list[Base]:
        """Create multiple instances and save to database asynchronously."""
        instances = cls.build_batch(size, **kwargs)
        db.add_all(instances)
        await db.commit()
        for instance in instances:
            await db.refresh(instance)
        return instances