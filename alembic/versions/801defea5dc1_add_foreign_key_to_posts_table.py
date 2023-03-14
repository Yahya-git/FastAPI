"""add foreign-key to posts table

Revision ID: 801defea5dc1
Revises: 1e2e567ce0a2
Create Date: 2023-03-03 17:50:57.500583

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "801defea5dc1"
down_revision = "1e2e567ce0a2"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("user_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        "post_users_fkey",
        source_table="posts",
        referent_table="users",
        local_cols=["user_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )
    pass


def downgrade() -> None:
    op.drop_constraint("post_users_fkey", table_name="posts")
    op.drop_column("posts", "user_id")
    pass
