"""empty message

Revision ID: 380cff300850
Revises: 
Create Date: 2020-12-24 23:45:25.874760

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '380cff300850'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('showss', sa.Column('comm', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('showss', 'comm')
    # ### end Alembic commands ###