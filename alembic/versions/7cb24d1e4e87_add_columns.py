"""add columns

Revision ID: 7cb24d1e4e87
Revises: 0dda025c8b92
Create Date: 2023-03-03 17:28:22.025998

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "7cb24d1e4e87"
down_revision = "0dda025c8b92"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
