"""empty message

Revision ID: 39480896bd81
Revises: 5047dfeaed2d
Create Date: 2016-09-16 16:56:43.168211

"""

# revision identifiers, used by Alembic.
revision = '39480896bd81'
down_revision = '5047dfeaed2d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('car', schema=None) as batch_op:
        batch_op.drop_column('current_mileage')

    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('car', schema=None) as batch_op:
        batch_op.add_column(sa.Column('current_mileage', sa.INTEGER(), nullable=True))

    ### end Alembic commands ###
