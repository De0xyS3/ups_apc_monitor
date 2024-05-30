"""Initial migration

Revision ID: bb23b203f972
Revises: 
Create Date: 2024-05-19 15:15:28.118888

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bb23b203f972'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('battery_threshold',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('threshold', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('host',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('ip_address', sa.String(length=64), nullable=True),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('password', sa.String(length=128), nullable=True),
    sa.Column('port', sa.Integer(), nullable=True),
    sa.Column('status', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('host', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_host_ip_address'), ['ip_address'], unique=False)
        batch_op.create_index(batch_op.f('ix_host_name'), ['name'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('host', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_host_name'))
        batch_op.drop_index(batch_op.f('ix_host_ip_address'))

    op.drop_table('host')
    op.drop_table('battery_threshold')
    # ### end Alembic commands ###
