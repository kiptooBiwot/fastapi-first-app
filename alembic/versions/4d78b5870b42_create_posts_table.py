"""create posts table

Revision ID: 4d78b5870b42
Revises: 
Create Date: 2023-08-23 13:09:49.822079

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4d78b5870b42"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer, nullable=False, primary_key=True),
        sa.Column("title", sa.String, nullable=False),
    )
    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass
