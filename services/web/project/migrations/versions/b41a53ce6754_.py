"""empty message

Revision ID: b41a53ce6754
Revises: 
Create Date: 2024-02-26 20:43:49.918909

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b41a53ce6754'
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
    op.create_table('web',
    sa.Column('film_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('release_date', sa.Date(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('rating', sa.Numeric(), nullable=False),
    sa.Column('poster', sa.String(), nullable=False),
    sa.Column('users_user_id', sa.Integer(), nullable=True),
    sa.Column('directors_director_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['directors_director_id'], ['directors.director_id'], ),
    sa.ForeignKeyConstraint(['users_user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('film_id')
    )
    op.create_table('film_genre',
    sa.Column('film_id', sa.Integer(), nullable=True),
    sa.Column('genre_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['film_id'], ['web.film_id'], ),
    sa.ForeignKeyConstraint(['genre_id'], ['genres.genre_id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('film_genre')
    op.drop_table('web')
    op.drop_table('users')
    op.drop_table('genres')
    op.drop_table('directors')
    # ### end Alembic commands ###
