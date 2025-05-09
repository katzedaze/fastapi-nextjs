from sqlalchemy import Column, String, Integer, Float, Text
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from app.models.base_model import BaseModel


class Item(Base, BaseModel):
    """Item model for storing item related data."""

    # テーブル名を明示的に指定
    __tablename__ = "items"

    name = Column(String(255), index=True, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    image_url = Column(String(255), nullable=True)

    # リレーションシップ
    order_items = relationship("OrderItem", back_populates="item")
