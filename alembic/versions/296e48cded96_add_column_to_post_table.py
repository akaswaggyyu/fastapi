"""add column to post table

Revision ID: 296e48cded96
Revises: 427db7de3a97
Create Date: 2022-02-09 16:02:05.511897

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '296e48cded96'
down_revision = '427db7de3a97'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
