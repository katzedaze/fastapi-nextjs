#!/usr/bin/env python

import asyncio
import sys
import logging
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import async_session_factory
from app.factories.factory_seeder import seed_users, seed_items, seed_orders_with_items
from app.models.user import User
from app.models.item import Item
from sqlalchemy import select

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def run_factory_seeder(seeder_name: str) -> None:
    """Run a specific factory seeder by name."""
    try:
        async with async_session_factory() as db:
            if seeder_name == "user":
                logger.info("Running user factory seeder...")
                users = await seed_users(db)
                logger.info(f"User factory seeder completed successfully. Created {len(users)} users.")
                
            elif seeder_name == "item":
                logger.info("Running item factory seeder...")
                items = await seed_items(db)
                logger.info(f"Item factory seeder completed successfully. Created {len(items)} items.")
                
            elif seeder_name == "order":
                logger.info("Running order factory seeder...")
                # Get existing users and items
                user_result = await db.execute(select(User))
                users = user_result.scalars().all()
                
                item_result = await db.execute(select(Item))
                items = item_result.scalars().all()
                
                if not users or not items:
                    logger.error("Users and items must exist before creating orders. Run user and item seeders first.")
                    sys.exit(1)
                
                orders = await seed_orders_with_items(db, users, items)
                logger.info(f"Order factory seeder completed successfully. Created {len(orders)} orders.")
                
            else:
                logger.error(f"Unknown factory seeder: {seeder_name}")
                logger.error("Available seeders: user, item, order")
                sys.exit(1)

    except Exception as e:
        logger.error(f"Error running {seeder_name} factory seeder: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        logger.error("Usage: python run_seeder.py [user|item|order]")
        logger.error("This script now uses SQLAlchemyModelFactory instead of legacy seeders")
        sys.exit(1)

    seeder_name = sys.argv[1].lower()
    asyncio.run(run_factory_seeder(seeder_name))
