"""created

Revision ID: c614df6873ce
Revises: a55c93c56ee9
Create Date: 2023-08-06 21:18:59.652998

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c614df6873ce'
down_revision = 'a55c93c56ee9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('quote_model', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('quote_model', schema=None) as batch_op:
        batch_op.drop_column('created')

    # ### end Alembic commands ###
