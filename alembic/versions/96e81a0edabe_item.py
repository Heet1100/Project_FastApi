"""item

Revision ID: 96e81a0edabe
Revises: 
Create Date: 2024-03-14 17:34:11.241583

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '96e81a0edabe'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() :
    op.create_table("item",
                    sa.Column("id",sa.Integer(),sa.PrimaryKeyConstraint("id") ),
                    sa.Column("name",sa.String(),nullable=False),
                    sa.Column("price",sa.Float(),nullable=False),
                    sa.Column("description",sa.String()),
                    sa.Column("store_id",sa.Integer(),sa.ForeignKey("store.id"),nullable=False))



def downgrade() :
    op.drop_table("items")
