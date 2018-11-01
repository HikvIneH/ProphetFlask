"""empty message

Revision ID: 06409d1a73df
Revises: 0b0b79fc5c21
Create Date: 2018-11-01 11:03:02.536204

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '06409d1a73df'
down_revision = '0b0b79fc5c21'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password', sa.String(length=80), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'password')
    # ### end Alembic commands ###
