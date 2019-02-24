"""empty message

Revision ID: 23a33503874f
Revises: a92edfa11544
Create Date: 2019-02-06 15:40:35.311422

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '23a33503874f'
down_revision = 'a92edfa11544'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('job_post', 'start_date')
    op.drop_column('job_post', 'end_date')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('job_post', sa.Column('end_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column('job_post', sa.Column('start_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###