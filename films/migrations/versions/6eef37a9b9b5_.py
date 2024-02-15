"""empty message

Revision ID: 6eef37a9b9b5
Revises: 
Create Date: 2024-02-15 17:02:51.833835

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6eef37a9b9b5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('directors',
    sa.Column('director_id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('date_of_birth', sa.Date(), nullable=False),
    sa.PrimaryKeyConstraint('director_id')
    )
    op.create_table('genres',
    sa.Column('genre_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('genre_id')
    )
    op.create_table('users',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('middle_name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('phone', sa.String(), nullable=False),
    sa.Column('is_admin', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_table('films',
    sa.Column('film_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('release_date', sa.Date(), nullable=False),
    sa.Column('descripion', sa.String(), nullable=True),
    sa.Column('rating', sa.Numeric(), nullable=False),
    sa.Column('poster', sa.String(), nullable=False),
    sa.Column('users_user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['users_user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('film_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('films')
    op.drop_table('users')
    op.drop_table('genres')
    op.drop_table('directors')
    # ### end Alembic commands ###
