"""add posted_at column to comments table

Revision ID: f2a167ddef8e
Revises: b41f608682de
Create Date: 2023-03-09 13:25:37.679675

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "f2a167ddef8e"
down_revision = "b41f608682de"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "comments",
        sa.Column(
            "posted_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
    )
    pass


def downgrade() -> None:
    op.drop_column("comments", "posted_at")
    pass
