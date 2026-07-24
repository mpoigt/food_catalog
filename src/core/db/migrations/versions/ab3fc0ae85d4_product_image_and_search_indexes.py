"""product image and search indexes

Revision ID: ab3fc0ae85d4
Revises: b42559d216ef
Create Date: 2026-07-24 03:03:08.895869

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'ab3fc0ae85d4'
down_revision: str | Sequence[str] | None = 'b42559d216ef'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('products', sa.Column('image_path', sa.String(length=512), nullable=True))

    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")
    op.execute(
        "CREATE INDEX ix_products_name_trgm "
        "ON products USING gin (name gin_trgm_ops)"
    )
    op.execute(
        "CREATE INDEX ix_products_description_trgm "
        "ON products USING gin (description gin_trgm_ops)"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP INDEX IF EXISTS ix_products_description_trgm")
    op.execute("DROP INDEX IF EXISTS ix_products_name_trgm")
    op.drop_column('products', 'image_path')
