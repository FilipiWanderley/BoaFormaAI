"""add user adaptive profiles

Revision ID: b71d4f9a2e63
Revises: 9a7c5e8b4d12
Create Date: 2026-04-01 12:10:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "b71d4f9a2e63"
down_revision: Union[str, None] = "9a7c5e8b4d12"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user_adaptive_profiles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("total_feedbacks", sa.Integer(), server_default=sa.text("0"), nullable=False),
        sa.Column("easy_count", sa.Integer(), server_default=sa.text("0"), nullable=False),
        sa.Column("ok_count", sa.Integer(), server_default=sa.text("0"), nullable=False),
        sa.Column("hard_count", sa.Integer(), server_default=sa.text("0"), nullable=False),
        sa.Column("last_feedback", sa.String(length=20), server_default=sa.text("''"), nullable=False),
        sa.Column("preferred_intensity", sa.String(length=30), server_default=sa.text("'balanced'"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id"),
    )
    op.create_index(op.f("ix_user_adaptive_profiles_id"), "user_adaptive_profiles", ["id"], unique=False)
    op.create_index(op.f("ix_user_adaptive_profiles_user_id"), "user_adaptive_profiles", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_user_adaptive_profiles_user_id"), table_name="user_adaptive_profiles")
    op.drop_index(op.f("ix_user_adaptive_profiles_id"), table_name="user_adaptive_profiles")
    op.drop_table("user_adaptive_profiles")
