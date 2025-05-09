import uuid
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func


# 日本のタイムゾーン
JST = ZoneInfo("Asia/Tokyo")


class BaseModel:
    """Base model class that includes common columns for all models."""
    
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    
    # 現在時刻は日本時間で設定
    created_at = Column(
        DateTime, 
        default=lambda: datetime.now(JST).replace(tzinfo=None),
        nullable=False
    )
    
    updated_at = Column(
        DateTime, 
        default=lambda: datetime.now(JST).replace(tzinfo=None),
        onupdate=lambda: datetime.now(JST).replace(tzinfo=None),
        nullable=False
    )