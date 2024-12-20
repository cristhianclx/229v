"""empty message

Revision ID: c635c3ba45d2
Revises: 532aaa11a7af
Create Date: 2024-11-23 17:52:16.045570

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c635c3ba45d2'
down_revision = '532aaa11a7af'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('message', schema=None) as batch_op:
        batch_op.add_column(sa.Column('feedback', sa.String(length=150), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('message', schema=None) as batch_op:
        batch_op.drop_column('feedback')

    # ### end Alembic commands ###
