#!/usr/bin/env python

import asyncio
import sys
import logging
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import async_session_factory

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def run_seeder(seeder_name: str) -> None:
    """Run a specific seeder by name."""
    try:
        # Dynamically import the seeder
        if seeder_name == "user":
            from app.db.seeder.user_seeder import UserSeeder as Seeder
        elif seeder_name == "item":
            from app.db.seeder.item_seeder import ItemSeeder as Seeder
        elif seeder_name == "order":
            from app.db.seeder.order_seeder import OrderSeeder as Seeder
        else:
            logger.error(f"Unknown seeder: {seeder_name}")
            sys.exit(1)

        # Run the seeder
        async with async_session_factory() as db:
            logger.info(f"Running {seeder_name} seeder...")
            seeder = Seeder(db)
            await seeder.run()
            logger.info(f"{seeder_name.capitalize()} seeder completed successfully")
    except Exception as e:
        logger.error(f"Error running {seeder_name} seeder: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        logger.error("Usage: python run_seeder.py [user|item|order]")
        sys.exit(1)
    
    seeder_name = sys.argv[1].lower()
    asyncio.run(run_seeder(seeder_name))