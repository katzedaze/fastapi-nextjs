from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.seeder.base import BaseSeeder
from app.models.item import Item


class ItemSeeder(BaseSeeder):
    """Seeder for Item model."""

    model = Item

    async def run(self) -> None:
        """Create default items if they don't exist."""
        default_items = [
            {
                "name": "ノートパソコン",
                "description": "高性能なビジネス向けノートパソコン。16GBメモリ、512GB SSD搭載。",
                "price": 125000.0,
                "stock": 10,
                "image_url": "https://example.com/images/laptop.jpg",
            },
            {
                "name": "ワイヤレスイヤホン",
                "description": "ノイズキャンセリング機能付きの高音質ワイヤレスイヤホン。バッテリー持続時間8時間。",
                "price": 15000.0,
                "stock": 25,
                "image_url": "https://example.com/images/earphones.jpg",
            },
            {
                "name": "スマートウォッチ",
                "description": "健康管理機能付きのスマートウォッチ。心拍数、睡眠管理、歩数計測が可能。",
                "price": 22000.0,
                "stock": 15,
                "image_url": "https://example.com/images/smartwatch.jpg",
            },
            {
                "name": "デスクトップPC",
                "description": "ゲーミング用高性能デスクトップPC。RTX 3080搭載、水冷システム。",
                "price": 250000.0,
                "stock": 5,
                "image_url": "https://example.com/images/desktop.jpg",
            },
            {
                "name": "Bluetoothスピーカー",
                "description": "コンパクトで持ち運びに便利なBluetoothスピーカー。防水機能付き。",
                "price": 8000.0,
                "stock": 30,
                "image_url": "https://example.com/images/speaker.jpg",
            },
        ]

        # すでに商品が存在する場合はシードしない
        result = await self.db.execute(select(Item))
        existing_items = result.scalars().all()

        if not existing_items:
            await self.create_many(default_items)

        # 特定の商品が存在するか確認してから追加する方法
        # for item_data in default_items:
        #     result = await self.db.execute(
        #         select(Item).where(Item.name == item_data["name"])
        #     )
        #     existing_item = result.scalars().first()
        #
        #     if not existing_item:
        #         await self.create(item_data)
