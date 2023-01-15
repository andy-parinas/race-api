"""add win_ratio column to current_race

Revision ID: 72a757444334
Revises: efe65050196b
Create Date: 2023-01-14 15:20:37.348640

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '72a757444334'
down_revision = 'efe65050196b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('currentrace', sa.Column('win_ratio', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('currentrace', 'win_ratio')
    # ### end Alembic commands ###