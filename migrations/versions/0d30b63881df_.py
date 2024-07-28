"""empty message

Revision ID: 0d30b63881df
Revises: afedfcb07a8b
Create Date: 2024-07-24 20:09:19.071947

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0d30b63881df'
down_revision = 'afedfcb07a8b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorites', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id_character', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'character', ['id_character'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorites', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('id_character')

    # ### end Alembic commands ###
