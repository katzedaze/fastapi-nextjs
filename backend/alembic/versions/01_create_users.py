"""create_users_table

Revision ID: 01_create_users
Revises: 
Create Date: 2025-05-09 21:15:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '01_create_users'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ユーザーテーブルの作成
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('email', sa.String(), nullable=False, unique=True, index=True),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('full_name', sa.String(), nullable=True, index=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('is_superuser', sa.Boolean(), nullable=False, server_default=sa.text('false')),
    )
    
    # インデックスの作成
    op.create_index('ix_users_id', 'users', ['id'], unique=False)


def downgrade() -> None:
    # テーブル削除
    op.drop_table('users')
