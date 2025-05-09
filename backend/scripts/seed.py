import asyncio
import logging
from typing import List, Type

import typer
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.seeder.base import BaseSeeder
from app.db.seeder.user_seeder import UserSeeder
from app.db.seeder.item_seeder import ItemSeeder
from app.db.seeder.order_seeder import OrderSeeder
from app.db.session import async_session_factory

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create typer app
app = typer.Typer()

# List of seeders to run
seeders: List[Type[BaseSeeder]] = [
    UserSeeder,
    ItemSeeder,
    OrderSeeder,
    # Add more seeders here as you create them
]


async def run_seeders() -> None:
    """Run all the seeders."""
    async with async_session_factory() as db:
        for seeder_class in seeders:
            logger.info(f"Running seeder: {seeder_class.__name__}")
            seeder = seeder_class(db)
            try:
                await seeder.run()
                logger.info(
                    f"Seeder {seeder_class.__name__} completed successfully")
            except Exception as e:
                logger.error(f"Error running {seeder_class.__name__}: {e}")
                raise


@app.command()
def seed() -> None:
    """Run all database seeders."""
    logger.info("Starting database seeding...")
    try:
        asyncio.run(run_seeders())
        logger.info("Database seeding completed successfully")
    except Exception as e:
        logger.error(f"Database seeding failed: {e}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
