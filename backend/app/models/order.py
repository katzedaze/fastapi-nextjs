from sqlalchemy import Column, String, Float, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import enum

from app.db.base_class import Base
from app.models.base_model import BaseModel


class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class Order(Base, BaseModel):
    """Order model for storing order related data."""

    # テーブル名を明示的に指定
    __tablename__ = "orders"

    user_id = Column(UUID(as_uuid=True), ForeignKey(
        "users.id"), nullable=False)
    status = Column(Enum(OrderStatus, values_callable=lambda obj: [e.value for e in obj]),
                    default=OrderStatus.PENDING, nullable=False)
    shipping_address = Column(Text, nullable=True)
    total_amount = Column(Float, nullable=False)
    notes = Column(Text, nullable=True)

    # リレーションシップ
    user = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")

    @property
    def items(self):
        return [order_item.item for order_item in self.order_items]
