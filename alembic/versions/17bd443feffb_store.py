"""store

Revision ID: 17bd443feffb
Revises: 96e81a0edabe
Create Date: 2024-03-14 18:22:58.911164

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '17bd443feffb'
down_revision: Union[str, None] = '96e81a0edabe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() :
    op.create_table('store',
                    sa.Column('store_id',sa.Integer(), primary_key=True),
                    sa.Column('name', sa.String(), nullable=False))


def downgrade() :
    op.drop_table("store")
