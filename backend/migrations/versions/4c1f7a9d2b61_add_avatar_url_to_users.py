"""add avatar_url to users

Revision ID: 4c1f7a9d2b61
Revises: e2a4f8c1d903
Create Date: 2026-04-01 03:20:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "4c1f7a9d2b61"
down_revision: Union[str, None] = "e2a4f8c1d903"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.add_column(sa.Column("avatar_url", sa.Text(), nullable=True))


def downgrade() -> None:
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.drop_column("avatar_url")
