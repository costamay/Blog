"""Initial Migration

Revision ID: ad31ab9062a4
Revises: 05a92de8863a
Create Date: 2019-10-27 12:47:06.075153

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ad31ab9062a4'
down_revision = '05a92de8863a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'comments', 'users', ['user_id'], ['id'])
    op.drop_column('comments', 'username')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('username', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'comments', type_='foreignkey')
    op.drop_column('comments', 'user_id')
    # ### end Alembic commands ###
