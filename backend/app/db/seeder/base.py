from datetime import datetime
from typing import Any, Dict, List, Optional, Type
from zoneinfo import ZoneInfo

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base_class import Base


JST = ZoneInfo("Asia/Tokyo")


class BaseSeeder:
    """Base seeder class that all seeders should inherit from."""

    model: Type[Base]

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, obj_in: Dict[str, Any]) -> Base:
        """Create a single record in the database."""
        # 現在時刻を日本時間で設定
        now = datetime.now(JST).replace(tzinfo=None)
        obj_data = {**obj_in}

        # created_at と updated_at が明示的に指定されていない場合は現在時刻を設定
        if "created_at" not in obj_data:
            obj_data["created_at"] = now
        if "updated_at" not in obj_data:
            obj_data["updated_at"] = now

        obj = self.model(**obj_data)
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def create_many(self, objects_in: List[Dict[str, Any]]) -> List[Base]:
        """Create multiple records in the database."""
        now = datetime.now(JST).replace(tzinfo=None)
        objects = []

        for obj_in in objects_in:
            obj_data = {**obj_in}
            if "created_at" not in obj_data:
                obj_data["created_at"] = now
            if "updated_at" not in obj_data:
                obj_data["updated_at"] = now

            obj = self.model(**obj_data)
            objects.append(obj)

        self.db.add_all(objects)
        await self.db.commit()
        for obj in objects:
            await self.db.refresh(obj)
        return objects

    async def run(self) -> None:
        """Method to be implemented by child seeders."""
        raise NotImplementedError("Seeders must implement run method")
