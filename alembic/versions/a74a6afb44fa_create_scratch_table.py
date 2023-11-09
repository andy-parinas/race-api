"""create scratch table

Revision ID: a74a6afb44fa
Revises: 839420a2e8b4
Create Date: 2023-11-09 20:00:09.423381

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a74a6afb44fa'
down_revision = '839420a2e8b4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('scratch_files',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('file_name', sa.String(), nullable=False),
    sa.Column('is_processed', sa.Boolean(), nullable=True),
    sa.Column('is_uploaded', sa.Boolean(), nullable=True),
    sa.Column('timestamp', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_scratch_files_id'), 'scratch_files', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_scratch_files_id'), table_name='scratch_files')
    op.drop_table('scratch_files')
    # ### end Alembic commands ###
