"""create_order_items_relation

Revision ID: 04_create_order_items
Revises: 03_create_orders
Create Date: 2025-05-09 21:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '04_create_order_items'
down_revision = '03_create_orders'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 注文-商品の中間テーブルの作成
    op.create_table(
        'order_items',
        sa.Column('order_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('orders.id'), primary_key=True),
        sa.Column('item_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('items.id'), primary_key=True),
        sa.Column('quantity', sa.Integer(), nullable=False,
                  server_default=sa.text('1')),
        sa.Column('price_at_time', sa.Float(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True),
                  server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(
        ), onupdate=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    # テーブル削除
    op.drop_table('order_items')
