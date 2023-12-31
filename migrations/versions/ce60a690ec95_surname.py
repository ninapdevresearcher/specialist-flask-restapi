"""surname

Revision ID: ce60a690ec95
Revises: 65fa9b51aeb5
Create Date: 2023-08-12 17:04:23.064151

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ce60a690ec95'
down_revision = '65fa9b51aeb5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('author_model', schema=None) as batch_op:
        batch_op.add_column(sa.Column('surname', sa.String(length=32), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('author_model', schema=None) as batch_op:
        batch_op.drop_column('surname')

    # ### end Alembic commands ###
