"""Add name column to User table

Revision ID: 366df0d6d438
Revises: 
Create Date: 2024-06-08 01:37:47.293714

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '366df0d6d438'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(length=20), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('name')

    # ### end Alembic commands ###
