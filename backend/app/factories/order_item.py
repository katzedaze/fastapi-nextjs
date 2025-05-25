import factory
from factory import Faker, SubFactory

from app.factories.base import BaseSQLAlchemyModelFactory
from app.factories.item import ItemFactory
from app.factories.order import OrderFactory
from app.models.order_item import OrderItem


class OrderItemFactory(BaseSQLAlchemyModelFactory):
    """Factory for OrderItem model."""

    class Meta:
        model = OrderItem

    order = SubFactory(OrderFactory)
    item = SubFactory(ItemFactory)
    quantity = Faker("pyint", min_value=1, max_value=5)
    
    @factory.lazy_attribute
    def order_id(self):
        return self.order.id if hasattr(self, 'order') and self.order else None
    
    @factory.lazy_attribute
    def item_id(self):
        return self.item.id if hasattr(self, 'item') and self.item else None
    
    @factory.lazy_attribute
    def price_at_time(self):
        return self.item.price if hasattr(self, 'item') and self.item else 1000.0