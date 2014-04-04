"""empty message

Revision ID: 36b5aaa11324
Revises: 40250febe7eb
Create Date: 2014-04-01 13:14:39.163985

"""

# revision identifiers, used by Alembic.
revision = '36b5aaa11324'
down_revision = '55e8cdb63057'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('packagehistory',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nodename', sa.String(length=255), nullable=True),
    sa.Column('pkgsha', sa.String(length=255), nullable=True),
    sa.Column('pkgname', sa.String(length=255), nullable=True),
    sa.Column('pkgversion', sa.String(length=64), nullable=True),
    sa.Column('pkgsource', sa.Text(), nullable=True),
    sa.Column('installed', sa.DATE(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('packagehistory')
    ### end Alembic commands ###
