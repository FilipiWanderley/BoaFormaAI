"""add lgpd fields to users

Revision ID: ab81d9f2c6e4
Revises: b3e9d1c4f220
Create Date: 2026-03-31 23:25:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ab81d9f2c6e4"
down_revision: Union[str, None] = "b3e9d1c4f220"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.add_column(sa.Column("consent_given_at", sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column("privacy_policy_version", sa.String(length=20), nullable=True))


def downgrade() -> None:
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.drop_column("privacy_policy_version")
        batch_op.drop_column("consent_given_at")
