"""add content column to post table

Revision ID: 43c715d1a9f5
Revises: 4d78b5870b42
Create Date: 2023-08-23 13:25:41.435484

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "43c715d1a9f5"
down_revision: Union[str, None] = "4d78b5870b42"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "posts",
        sa.Column("content", sa.String(), nullable=False),
    )
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
