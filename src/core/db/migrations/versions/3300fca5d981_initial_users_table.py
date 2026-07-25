"""initial users table

Revision ID: 3300fca5d981
Revises:
Create Date: 2026-07-20 22:24:52.853968

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "3300fca5d981"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column(
            "id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.Column("username", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column(
            "role", sa.Enum("USER", "ADVANCED", "ADMIN", name="role"), nullable=False
        ),
        sa.Column("is_blocked", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("username"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
