"""create_orders_table

Revision ID: 03_create_orders
Revises: 02_create_items
Create Date: 2025-05-09 21:25:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '03_create_orders'
down_revision = '02_create_items'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # すでにenumが作成されているため、注文テーブルのみ作成する
    # 注文テーブルの作成
    op.create_table(
        'orders',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('status', sa.Enum('pending', 'processing', 'shipped', 'delivered', 'cancelled', name='orderstatus', create_type=False), nullable=False, server_default='pending'),
        sa.Column('shipping_address', sa.Text(), nullable=True),
        sa.Column('total_amount', sa.Float(), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
    )
    
    # インデックスの作成
    op.create_index('ix_orders_id', 'orders', ['id'], unique=False)


def downgrade() -> None:
    # テーブル削除
    op.drop_table('orders')
