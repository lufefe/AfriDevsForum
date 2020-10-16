"""empty message

Revision ID: ef8e70f0dee9
Revises: dee395baf7a1
Create Date: 2020-08-23 00:50:14.765497

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'ef8e70f0dee9'
down_revision = 'dee395baf7a1'
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
    op.drop_index('ix_roles_default', table_name = 'roles')
    op.drop_table('roles')
    op.drop_index('ix_comments_timestamp', table_name = 'comments')
    op.drop_table('comments')
    op.add_column('user', sa.Column('about_me', sa.Text(), nullable = True))
    op.add_column('user', sa.Column('member_since', sa.DateTime(), nullable = True))
    op.create_foreign_key(None, 'user', 'role', ['role_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_ = 'foreignkey')
    op.drop_column('user', 'member_since')
    op.drop_column('user', 'about_me')
    op.create_table('comments',
                    sa.Column('id', sa.INTEGER(), nullable = False),
                    sa.Column('body', sa.TEXT(), nullable = True),
                    sa.Column('body_html', sa.TEXT(), nullable = True),
                    sa.Column('timestamp', sa.DATETIME(), nullable = True),
                    sa.Column('disabled', sa.BOOLEAN(), nullable = True),
                    sa.Column('author_id', sa.INTEGER(), nullable = True),
                    sa.Column('post_id', sa.INTEGER(), nullable = True),
                    sa.CheckConstraint('disabled IN (0, 1)'),
                    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
                    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index('ix_comments_timestamp', 'comments', ['timestamp'], unique = False)
    op.create_table('roles',
                    sa.Column('id', sa.INTEGER(), nullable = False),
                    sa.Column('name', sa.VARCHAR(length = 64), nullable = True),
                    sa.Column('default', sa.BOOLEAN(), nullable = True),
                    sa.Column('permissions', sa.INTEGER(), nullable = True),
                    sa.CheckConstraint('"default" IN (0, 1)'),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('name')
                    )
    op.create_index('ix_roles_default', 'roles', ['default'], unique = False)
    op.drop_index(op.f('ix_comment_timestamp'), table_name = 'comment')
    op.drop_table('comment')
    op.drop_index(op.f('ix_role_default'), table_name = 'role')
    op.drop_table('role')
    # ### end Alembic commands ###
