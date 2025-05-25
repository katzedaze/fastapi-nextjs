import random
from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.factories.user import UserFactory, AdminUserFactory
from app.factories.item import (
    ItemFactory, LaptopFactory, EarphonesFactory, 
    SmartwatchFactory, DesktopFactory, SpeakerFactory
)
from app.factories.order import OrderFactory
from app.factories.order_item import OrderItemFactory
from app.models.user import User
from app.models.item import Item
from app.models.order import Order
from app.models.order_item import OrderItem


async def seed_users(db: AsyncSession) -> List[User]:
    """Seed users using factories."""
    # Check if admin user exists
    result = await db.execute(
        select(User).where(User.email == "admin@example.com")
    )
    existing_admin = result.scalars().first()

    users = []
    
    if not existing_admin:
        # Create admin user
        admin = await AdminUserFactory.create_async(db)
        users.append(admin)

    # Create test users
    test_users = await UserFactory.create_batch_async(
        db, 2, 
        email=lambda: f"user{random.randint(1,100)}@example.com"
    )
    users.extend(test_users)
    
    return users


async def seed_items(db: AsyncSession) -> List[Item]:
    """Seed items using factories."""
    # Check if items already exist
    result = await db.execute(select(Item))
    existing_items = result.scalars().all()

    if existing_items:
        return existing_items

    # Create predefined items using specific factories
    items = []
    predefined_factories = [
        LaptopFactory,
        EarphonesFactory, 
        SmartwatchFactory,
        DesktopFactory,
        SpeakerFactory
    ]
    
    for factory_class in predefined_factories:
        item = await factory_class.create_async(db)
        items.append(item)
    
    return items


async def seed_orders_with_items(db: AsyncSession, users: List[User], items: List[Item]) -> List[Order]:
    """Seed orders with order items using factories."""
    # Check if orders already exist
    result = await db.execute(select(Order))
    existing_orders = result.scalars().all()

    if existing_orders:
        return existing_orders

    orders = []
    
    for user in users:
        # Create 1-3 orders per user
        num_orders = random.randint(1, 3)
        
        for _ in range(num_orders):
            # Create order without items first
            order = OrderFactory.build(user_id=user.id)
            
            # Select random items for this order
            selected_items = random.sample(items, random.randint(1, min(4, len(items))))
            
            # Calculate total amount and create order items
            total_amount = 0
            order_items_data = []
            
            for item in selected_items:
                quantity = random.randint(1, 3)
                item_total = item.price * quantity
                total_amount += item_total
                
                order_items_data.append({
                    "item": item,
                    "quantity": quantity,
                    "price_at_time": item.price
                })
            
            # Set calculated total amount
            order.total_amount = total_amount
            
            # Save order
            db.add(order)
            await db.commit()
            await db.refresh(order)
            
            # Create order items
            for item_data in order_items_data:
                order_item = OrderItem(
                    order_id=order.id,
                    item_id=item_data["item"].id,
                    quantity=item_data["quantity"],
                    price_at_time=item_data["price_at_time"]
                )
                db.add(order_item)
            
            await db.commit()
            orders.append(order)
    
    return orders


async def run_factory_seeder(db: AsyncSession) -> None:
    """Run complete seeding using factories."""
    print("Seeding users...")
    users = await seed_users(db)
    print(f"Created {len(users)} users")
    
    print("Seeding items...")
    items = await seed_items(db)
    print(f"Created {len(items)} items")
    
    print("Seeding orders with items...")
    orders = await seed_orders_with_items(db, users, items)
    print(f"Created {len(orders)} orders")
    
    print("Factory seeding completed successfully!")