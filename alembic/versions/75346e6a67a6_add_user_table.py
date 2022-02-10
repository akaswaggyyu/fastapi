"""add user table

Revision ID: 75346e6a67a6
Revises: 296e48cded96
Create Date: 2022-02-10 10:17:20.673627

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '75346e6a67a6'
down_revision = '296e48cded96'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('email', sa.String(), nullable=False),
            sa.Column('password', sa.String(), nullable=False),
            sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                        server_default=sa.text('now()') , nullable=False),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('email')
    )
    pass


def downgrade():
    op.drop_table('users')
    pass
