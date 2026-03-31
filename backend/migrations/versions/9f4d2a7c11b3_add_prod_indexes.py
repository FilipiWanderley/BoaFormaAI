"""add production indexes

Revision ID: 9f4d2a7c11b3
Revises: 2f3c9b10a7d1
Create Date: 2026-03-31 18:25:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "9f4d2a7c11b3"
down_revision: Union[str, None] = "2f3c9b10a7d1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index(
        "ix_workouts_user_created_at",
        "workouts",
        ["user_id", "created_at"],
        unique=False,
    )
    op.create_index(
        "ix_history_user_completed_at",
        "history",
        ["user_id", "completed_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_history_user_completed_at", table_name="history")
    op.drop_index("ix_workouts_user_created_at", table_name="workouts")
