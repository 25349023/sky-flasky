"""empty message

Revision ID: 18490e22770a
Revises: cabf6c86f621
Create Date: 2019-07-19 22:41:48.824635

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '18490e22770a'
down_revision = 'cabf6c86f621'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('confirmed', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'confirmed')
    # ### end Alembic commands ###
