"""create comments table

Revision ID: b41f608682de
Revises: f0746d9359ca
Create Date: 2023-03-09 12:23:40.363149

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b41f608682de'
down_revision = 'f0746d9359ca'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('comments',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('post_id', sa.Integer(), nullable=False),
                    sa.Column('comment', sa.String(), nullable=False),
                    sa.ForeignKeyConstraint(
                        ['post_id'], ['posts.id'], ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(
                        ['user_id'], ['users.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id'))
    pass


def downgrade() -> None:
    op.drop_table('comments')
    pass
