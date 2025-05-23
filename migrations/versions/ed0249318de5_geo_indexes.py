"""geo_indexes

Revision ID: ed0249318de5
Revises: 6b2b4297acec
Create Date: 2025-05-23 17:33:32.710358

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ed0249318de5'
down_revision: Union[str, None] = '6b2b4297acec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_index(
        "ix_geo_location",
        "geo",
        ["location"],
        unique=False,
        postgresql_using="gist",
        postgresql_ops={},
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(
        "ix_geo_location",
        table_name="geo",
        postgresql_using="gist",
        postgresql_ops={},
    )
