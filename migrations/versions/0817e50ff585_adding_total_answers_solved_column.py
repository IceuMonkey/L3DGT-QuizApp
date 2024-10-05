"""Adding total answers solved column

Revision ID: 0817e50ff585
Revises: ce7629933109
Create Date: 2024-10-04 19:58:23.430641

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0817e50ff585'
down_revision = 'ce7629933109'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('total_solved', sa.Integer(), nullable=True))
        batch_op.create_unique_constraint(batch_op.f('uq_users_email'), ['email'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_users_email'), type_='unique')
        batch_op.drop_column('total_solved')

    # ### end Alembic commands ###
