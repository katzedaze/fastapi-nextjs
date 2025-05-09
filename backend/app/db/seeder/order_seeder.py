import random
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.seeder.base import BaseSeeder
from app.models.order import Order, OrderStatus
from app.models.order_item import OrderItem
from app.models.user import User
from app.models.item import Item
# import enum


# class OrderStatus(str, enum.Enum):
#     PENDING = "pending"
#     PROCESSING = "processing"
#     SHIPPED = "shipped"
#     DELIVERED = "delivered"
#     CANCELLED = "cancelled"


class OrderSeeder(BaseSeeder):
    """Seeder for Order model."""

    model = Order

    async def run(self) -> None:
        """Create sample orders if they don't exist."""
        # すでに注文が存在する場合はシードしない
        result = await self.db.execute(select(Order))
        existing_orders = result.scalars().all()

        if existing_orders:
            return

        # ユーザーとアイテムの取得
        user_result = await self.db.execute(select(User))
        users = user_result.scalars().all()

        item_result = await self.db.execute(select(Item))
        items = item_result.scalars().all()

        if not users or not items:
            return

        # サンプル注文データ作成
        for user in users:
            # 各ユーザーに1〜3件の注文を作成
            for _ in range(random.randint(1, 3)):
                # 各注文に1〜4個のアイテムをランダムに選択
                selected_items = random.sample(
                    items, random.randint(1, min(4, len(items))))

                # 注文の合計金額を計算
                total_amount = 0
                order_items_data = []

                for item in selected_items:
                    quantity = random.randint(1, 3)
                    item_total = item.price * quantity
                    total_amount += item_total

                    order_items_data.append({
                        "item_id": item.id,
                        "quantity": quantity,
                        "price_at_time": item.price
                    })

                # 注文作成（OrderStatus enumを使用）
                status_value = random.choice([
                    OrderStatus.PENDING.value,  # "pending"
                    OrderStatus.PROCESSING.value,  # "processing"
                    OrderStatus.SHIPPED.value,  # "shipped"
                    OrderStatus.DELIVERED.value,  # "delivered"
                    OrderStatus.CANCELLED.value  # "cancelled"
                ])
                # status_value = random.choice(list(OrderStatus))

                order_data = {
                    "user_id": user.id,
                    "status": status_value,
                    "shipping_address": f"{user.full_name}の配送先住所、東京都渋谷区...",
                    "total_amount": total_amount,
                    "notes": "特記事項なし" if random.random() > 0.5 else "午前中の配達希望"
                }

                # 注文を作成
                order = await self.create(order_data)

                # 注文アイテムの中間テーブルにデータを挿入
                for item_data in order_items_data:
                    order_item = OrderItem(
                        order_id=order.id,
                        item_id=item_data["item_id"],
                        quantity=item_data["quantity"],
                        price_at_time=item_data["price_at_time"]
                    )
                    self.db.add(order_item)

                await self.db.commit()
