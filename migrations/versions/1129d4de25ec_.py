"""empty message

Revision ID: 1129d4de25ec
Revises: ab97844e3a19
Create Date: 2020-08-23 19:42:26.460119

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '1129d4de25ec'
down_revision = 'ab97844e3a19'
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
