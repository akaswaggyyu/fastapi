"""add foreign key to posts table

Revision ID: 982563d1b283
Revises: 75346e6a67a6
Create Date: 2022-02-10 10:25:57.477056

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '982563d1b283'
down_revision = '75346e6a67a6'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users",
            local_cols=['user_id'], remote_cols=['id'], ondelete="CASCADE" )
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'user_id')
    pass
