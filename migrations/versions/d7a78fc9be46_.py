"""empty message

Revision ID: d7a78fc9be46
Revises: None
Create Date: 2016-04-12 09:48:34.416919

"""

# revision identifiers, used by Alembic.
revision = 'd7a78fc9be46'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('entry', sa.Column('status', sa.SmallInteger(), server_default='0'))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('entry', 'status')
    ### end Alembic commands ###
