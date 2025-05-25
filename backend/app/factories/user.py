import factory
from factory import Faker

from app.core.security import get_password_hash
from app.factories.base import BaseSQLAlchemyModelFactory
from app.models.user import User


class UserFactory(BaseSQLAlchemyModelFactory):
    """Factory for User model."""

    class Meta:
        model = User

    email = Faker("email")
    full_name = Faker("name")
    is_active = True
    is_superuser = False

    @factory.lazy_attribute
    def hashed_password(self):
        return get_password_hash("password")


class AdminUserFactory(UserFactory):
    """Factory for admin users."""
    
    email = "admin@example.com"
    full_name = "Admin User"
    is_superuser = True
    is_active = True

    @factory.lazy_attribute
    def hashed_password(self):
        return get_password_hash("admin")