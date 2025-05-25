import asyncio
import logging

import typer
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import async_session_factory
from app.factories.factory_seeder import run_factory_seeder

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create typer app
app = typer.Typer()


async def run_seeding() -> None:
    """Run the factory-based seeding."""
    async with async_session_factory() as db:
        try:
            await run_factory_seeder(db)
            logger.info("Factory-based seeding completed successfully")
        except Exception as e:
            logger.error(f"Factory-based seeding failed: {e}")
            raise


@app.command()
def seed() -> None:
    """Run factory-based database seeding."""
    logger.info("Starting factory-based database seeding...")
    try:
        asyncio.run(run_seeding())
    except Exception as e:
        logger.error(f"Database seeding failed: {e}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()