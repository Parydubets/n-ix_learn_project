"""empty message

Revision ID: 5f73f261c719
Revises: 6eef37a9b9b5
Create Date: 2024-02-15 17:05:09.230606

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5f73f261c719'
down_revision = '6eef37a9b9b5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('films', schema=None) as batch_op:
        batch_op.add_column(sa.Column('directors_director_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'directors', ['directors_director_id'], ['director_id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('films', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('directors_director_id')

    # ### end Alembic commands ###
