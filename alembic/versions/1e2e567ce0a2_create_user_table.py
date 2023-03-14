"""create user table

Revision ID: 1e2e567ce0a2
Revises: 7cb24d1e4e87
Create Date: 2023-03-03 17:34:10.572426

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "1e2e567ce0a2"
down_revision = "7cb24d1e4e87"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
