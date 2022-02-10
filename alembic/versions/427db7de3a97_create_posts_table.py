"""create posts table

Revision ID: 427db7de3a97
Revises: 
Create Date: 2022-02-09 15:41:25.178572

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '427db7de3a97'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
