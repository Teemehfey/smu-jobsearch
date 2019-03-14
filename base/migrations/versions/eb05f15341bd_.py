"""empty message

Revision ID: eb05f15341bd
Revises: 616e44f531b7
Create Date: 2019-03-14 07:16:19.295492

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb05f15341bd'
down_revision = '616e44f531b7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('application', sa.Column('reject_reason', sa.String(length=32), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('application', 'reject_reason')
    # ### end Alembic commands ###
