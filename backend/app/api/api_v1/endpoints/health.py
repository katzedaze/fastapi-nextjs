from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

router = APIRouter()


@router.get("")
async def health_check(db: AsyncSession = Depends(get_db)):
    try:
        # Check database connection
        result = await db.execute("SELECT 1")
        if result.scalar() == 1:
            db_status = "ok"
        else:
            db_status = "error"
    except Exception:
        db_status = "error"

    return {
        "status": "ok",
        "database": db_status,
    }
