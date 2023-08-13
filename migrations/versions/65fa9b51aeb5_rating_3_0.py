"""rating 3.0

Revision ID: 65fa9b51aeb5
Revises: c614df6873ce
Create Date: 2023-08-07 00:58:46.161708

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '65fa9b51aeb5'
down_revision = 'c614df6873ce'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('quote_model', schema=None) as batch_op:
        batch_op.add_column(sa.Column('rating', sa.Integer(), server_default='1', nullable=False))
        batch_op.drop_column('rate')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('quote_model', schema=None) as batch_op:
        batch_op.add_column(sa.Column('rate', sa.INTEGER(), server_default=sa.text("'1'"), nullable=False))
        batch_op.drop_column('rating')

    # ### end Alembic commands ###
