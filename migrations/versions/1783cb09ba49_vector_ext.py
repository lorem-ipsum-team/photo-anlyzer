"""vector_ext

Revision ID: 1783cb09ba49
Revises: 52d8feac049f
Create Date: 2025-05-15 20:04:54.388957

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1783cb09ba49'
down_revision: Union[str, None] = '52d8feac049f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('CREATE EXTENSION IF NOT EXISTS "vector"')


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('DROP EXTENSION IF EXISTS "vector"')
