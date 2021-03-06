"""Create User model

Revision ID: 320cdefbd54f
Revises: b71ad72326d7
Create Date: 2022-02-04 17:40:18.698623

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '320cdefbd54f'
down_revision = 'b71ad72326d7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('hashed_password', sa.String(length=100), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.Column('joined', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('movies_x_users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('rate', sa.Float(), nullable=False),
    sa.Column('movie', sa.Integer(), nullable=True),
    sa.Column('user', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['movie'], ['movies.id'], name='fk_movies_x_users_movies_movie_id', onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user'], ['users.id'], name='fk_movies_x_users_users_user_id', onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('movies_x_users')
    op.drop_table('users')
    # ### end Alembic commands ###
