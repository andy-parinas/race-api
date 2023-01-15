"""add column to current meeting

Revision ID: efe65050196b
Revises: d26e004920f5
Create Date: 2023-01-14 13:08:11.604223

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'efe65050196b'
down_revision = 'd26e004920f5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('currentrace', sa.Column('meeting_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'currentrace', 'meeting', ['meeting_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'currentrace', type_='foreignkey')
    op.drop_column('currentrace', 'meeting_id')
    # ### end Alembic commands ###