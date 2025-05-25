import factory
from factory import Faker, SubFactory

from app.factories.base import BaseSQLAlchemyModelFactory
from app.factories.user import UserFactory
from app.models.order import Order, OrderStatus


class OrderFactory(BaseSQLAlchemyModelFactory):
    """Factory for Order model."""

    class Meta:
        model = Order

    user = SubFactory(UserFactory)
    status = Faker("random_element", elements=[status.value for status in OrderStatus])
    shipping_address = Faker("address")
    total_amount = Faker("pyfloat", positive=True, max_value=500000, right_digits=2)
    notes = Faker("random_element", elements=["特記事項なし", "午前中の配達希望", ""])

    @factory.lazy_attribute
    def user_id(self):
        return self.user.id if hasattr(self, 'user') and self.user else None


class PendingOrderFactory(OrderFactory):
    """Factory for pending orders."""
    
    status = OrderStatus.PENDING


class ProcessingOrderFactory(OrderFactory):
    """Factory for processing orders."""
    
    status = OrderStatus.PROCESSING


class ShippedOrderFactory(OrderFactory):
    """Factory for shipped orders."""
    
    status = OrderStatus.SHIPPED


class DeliveredOrderFactory(OrderFactory):
    """Factory for delivered orders."""
    
    status = OrderStatus.DELIVERED


class CancelledOrderFactory(OrderFactory):
    """Factory for cancelled orders."""
    
    status = OrderStatus.CANCELLED