"""Changed field type

Revision ID: 39d65cc90f74
Revises: fb8a896d98df
Create Date: 2025-05-30 19:33:43.422853

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '39d65cc90f74'
down_revision: Union[str, None] = 'fb8a896d98df'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('chat_members')
    op.drop_table('messages')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('messages',
    sa.Column('id', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('chat_id', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('sender_id', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('text', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('timestamp', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('is_read', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('messages_pkey'))
    )
    op.create_table('chat_members',
    sa.Column('chat_id', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('chat_id', name=op.f('chat_members_pkey'))
    )
    # ### end Alembic commands ###
