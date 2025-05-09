"""create_items_table

Revision ID: 02_create_items
Revises: 01_create_users
Create Date: 2025-05-09 21:20:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '02_create_items'
down_revision = '01_create_users'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 商品テーブルの作成
    op.create_table(
        'items',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True,
                  server_default=sa.text('gen_random_uuid()')),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('name', sa.String(255), nullable=False, index=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('stock', sa.Integer(), nullable=False,
                  server_default=sa.text('0')),
        sa.Column('image_url', sa.String(255), nullable=True),
    )

    # インデックスの作成
    op.create_index('ix_items_id', 'items', ['id'], unique=False)


def downgrade() -> None:
    # テーブル削除
    op.drop_table('items')
