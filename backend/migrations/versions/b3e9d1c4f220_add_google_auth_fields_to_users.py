"""add google auth fields to users

Revision ID: b3e9d1c4f220
Revises: 9f4d2a7c11b3
Create Date: 2026-03-31 21:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b3e9d1c4f220"
down_revision: Union[str, None] = "9f4d2a7c11b3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.add_column(sa.Column("provider", sa.String(length=20), nullable=False, server_default="email"))
        batch_op.add_column(sa.Column("provider_id", sa.String(length=255), nullable=True))
        batch_op.alter_column("hashed_password", existing_type=sa.String(length=255), nullable=True)
        batch_op.create_index(batch_op.f("ix_users_provider_id"), ["provider_id"], unique=True)


def downgrade() -> None:
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_users_provider_id"))
        batch_op.alter_column("hashed_password", existing_type=sa.String(length=255), nullable=False)
        batch_op.drop_column("provider_id")
        batch_op.drop_column("provider")
