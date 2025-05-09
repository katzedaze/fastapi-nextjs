from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash
from app.db.seeder.base import BaseSeeder
from app.models.user import User


class UserSeeder(BaseSeeder):
    """Seeder for User model."""

    model = User

    async def run(self) -> None:
        """Create default users if they don't exist."""
        default_users = [
            {
                "email": "admin@example.com",
                "hashed_password": get_password_hash("admin"),
                "full_name": "Admin User",
                "is_superuser": True,
                "is_active": True,
            },
            {
                "email": "user1@example.com",
                "hashed_password": get_password_hash("password"),
                "full_name": "Test User 1",
                "is_superuser": False,
                "is_active": True,
            },
            {
                "email": "user2@example.com",
                "hashed_password": get_password_hash("password"),
                "full_name": "Test User 2",
                "is_superuser": False,
                "is_active": True,
            },
        ]

        for user_data in default_users:
            # メールアドレスで既存ユーザーを検索
            result = await self.db.execute(
                select(User).where(User.email == user_data["email"])
            )
            existing_user = result.scalars().first()

            # ユーザーが存在しない場合のみ作成
            if not existing_user:
                await self.create(user_data)
