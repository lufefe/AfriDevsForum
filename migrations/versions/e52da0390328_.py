"""empty message

Revision ID: e52da0390328
Revises: 0d570b9a7857
Create Date: 2020-10-15 17:33:42.990536

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'e52da0390328'
down_revision = '0d570b9a7857'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('role',
                    sa.Column('id', sa.Integer(), nullable = False),
                    sa.Column('name', sa.String(length = 64), nullable = True),
                    sa.Column('default', sa.Boolean(), nullable = True),
                    sa.Column('permissions', sa.Integer(), nullable = True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('name')
                    )
    op.create_index(op.f('ix_role_default'), 'role', ['default'], unique = False)
    op.create_table('tag',
                    sa.Column('id', sa.Integer(), nullable = False),
                    sa.Column('name', sa.String(length = 64), nullable = True),
                    sa.Column('slug', sa.String(length = 64), nullable = True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('user',
                    sa.Column('id', sa.Integer(), nullable = False),
                    sa.Column('name', sa.String(length = 64), nullable = True),
                    sa.Column('username', sa.String(length = 20), nullable = False),
                    sa.Column('email', sa.String(length = 120), nullable = False),
                    sa.Column('country', sa.String(length = 20), nullable = False),
                    sa.Column('about_me', sa.Text(), nullable = True),
                    sa.Column('member_since', sa.DateTime(), nullable = True),
                    sa.Column('image_file', sa.String(length = 20), nullable = False),
                    sa.Column('password', sa.String(length = 60), nullable = True),
                    sa.Column('confirmed', sa.Boolean(), nullable = True),
                    sa.Column('role_id', sa.Integer(), nullable = True),
                    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'),
                    sa.UniqueConstraint('username')
                    )
    op.create_table('post',
                    sa.Column('id', sa.Integer(), nullable = False),
                    sa.Column('title', sa.String(length = 100), nullable = False),
                    sa.Column('date_posted', sa.DateTime(), nullable = False),
                    sa.Column('content', sa.Text(), nullable = False),
                    sa.Column('user_id', sa.Integer(), nullable = False),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('comment',
                    sa.Column('id', sa.Integer(), nullable = False),
                    sa.Column('body', sa.Text(), nullable = True),
                    sa.Column('body_html', sa.Text(), nullable = True),
                    sa.Column('timestamp', sa.DateTime(), nullable = True),
                    sa.Column('disabled', sa.Boolean(), nullable = True),
                    sa.Column('author_id', sa.Integer(), nullable = True),
                    sa.Column('post_id', sa.Integer(), nullable = True),
                    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
                    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_comment_timestamp'), 'comment', ['timestamp'], unique = False)
    op.create_table('post_tag',
                    sa.Column('tag_id', sa.Integer(), nullable = True),
                    sa.Column('post_id', sa.Integer(), nullable = True),
                    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
                    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], )
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post_tag')
    op.drop_index(op.f('ix_comment_timestamp'), table_name = 'comment')
    op.drop_table('comment')
    op.drop_table('post')
    op.drop_table('user')
    op.drop_table('tag')
    op.drop_index(op.f('ix_role_default'), table_name = 'role')
    op.drop_table('role')
    # ### end Alembic commands ###