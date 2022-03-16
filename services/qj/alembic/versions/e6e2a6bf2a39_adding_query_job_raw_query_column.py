"""Adding query job 'raw_query' column

Revision ID: e6e2a6bf2a39
Revises: 9d956e753055
Create Date: 2022-03-03 10:00:38.059957

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e6e2a6bf2a39'
down_revision = '9d956e753055'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('job', sa.Column('raw_query', sa.Boolean(), server_default='false', nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('job', 'raw_query')
    # ### end Alembic commands ###