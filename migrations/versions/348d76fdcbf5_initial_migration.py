"""Initial migration.

Revision ID: 348d76fdcbf5
Revises: 
Create Date: 2024-09-11 21:02:47.100011

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '348d76fdcbf5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('highscore', sa.Integer(), nullable=True))
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.String(length=150),
               existing_nullable=True)
        batch_op.create_unique_constraint(None, ['email'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.alter_column('email',
               existing_type=sa.String(length=150),
               type_=sa.VARCHAR(length=100),
               existing_nullable=True)
        batch_op.drop_column('highscore')

    # ### end Alembic commands ###
