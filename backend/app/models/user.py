from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.base_model import BaseModel


class User(Base, BaseModel):
    """User model for storing user related data."""

    # テーブル名を明示的に指定
    __tablename__ = "users"

    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, index=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    # リレーションシップ
    orders = relationship("Order", back_populates="user")