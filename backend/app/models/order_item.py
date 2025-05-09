from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.db.base_class import Base


class OrderItem(Base):
    """OrderItem model for storing order-item relationship data."""

    # テーブル名を明示的に指定
    __tablename__ = "order_items"

    # Primary key using composite key
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), primary_key=True, nullable=False)
    item_id = Column(UUID(as_uuid=True), ForeignKey("items.id"), primary_key=True, nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    price_at_time = Column(Float, nullable=False)  # 購入時の価格を保存

    # Add created_at and updated_at for consistency with other models
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # リレーションシップ
    order = relationship("Order", back_populates="order_items")
    item = relationship("Item", back_populates="order_items")