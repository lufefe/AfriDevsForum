"""empty message

Revision ID: 07c8200e91cc
Revises: 9a068e04dd67
Create Date: 2020-08-23 18:49:19.334962

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '07c8200e91cc'
down_revision = '9a068e04dd67'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'user', 'role', ['role_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_ = 'foreignkey')
    # ### end Alembic commands ###
