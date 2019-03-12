"""empty message

Revision ID: 0652eaa5d350
Revises: 2081224efc0d
Create Date: 2019-03-04 04:50:50.990927

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0652eaa5d350'
down_revision = '2081224efc0d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('jobpost', sa.Column('keywords', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('jobpost', 'keywords')
    # ### end Alembic commands ###