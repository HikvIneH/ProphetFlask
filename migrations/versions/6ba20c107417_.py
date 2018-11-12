"""empty message

Revision ID: 6ba20c107417
Revises: 66e5cc80a503
Create Date: 2018-11-09 20:10:58.701992

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '6ba20c107417'
down_revision = '66e5cc80a503'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_files', sa.Column('user_id', sa.Integer(), nullable=True))
    op.drop_index('ix_user_files_name', table_name='user_files')
    op.create_index(op.f('ix_user_files_name'), 'user_files', ['name'], unique=False)
    op.create_foreign_key(None, 'user_files', 'users', ['user_id'], ['id'])
    op.drop_constraint(u'users_ibfk_1', 'users', type_='foreignkey')
    op.drop_column('users', 'user_file_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('user_file_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.create_foreign_key(u'users_ibfk_1', 'users', 'user_files', ['user_file_id'], ['id'])
    op.drop_constraint(None, 'user_files', type_='foreignkey')
    op.drop_index(op.f('ix_user_files_name'), table_name='user_files')
    op.create_index('ix_user_files_name', 'user_files', ['name'], unique=True)
    op.drop_column('user_files', 'user_id')
    # ### end Alembic commands ###