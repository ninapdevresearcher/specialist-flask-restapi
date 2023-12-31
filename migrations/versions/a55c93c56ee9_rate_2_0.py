"""rate 2.0

Revision ID: a55c93c56ee9
Revises: 29e9b1550378
Create Date: 2023-08-06 19:56:11.208269

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a55c93c56ee9'
down_revision = '29e9b1550378'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('quote_model', schema=None) as batch_op:
        batch_op.add_column(sa.Column('rate', sa.Integer(), server_default='1', nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('quote_model', schema=None) as batch_op:
        batch_op.drop_column('rate')

    # ### end Alembic commands ###
