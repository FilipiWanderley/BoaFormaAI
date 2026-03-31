"""add refresh token sessions

Revision ID: 2f3c9b10a7d1
Revises: 7ab27e153090
Create Date: 2026-03-31 17:40:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2f3c9b10a7d1"
down_revision: Union[str, None] = "7ab27e153090"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "refresh_token_sessions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("token_id", sa.String(length=64), nullable=False),
        sa.Column("expires_at", sa.DateTime(), nullable=False),
        sa.Column("revoked_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_refresh_token_sessions_expires_at"), "refresh_token_sessions", ["expires_at"], unique=False)
    op.create_index(op.f("ix_refresh_token_sessions_id"), "refresh_token_sessions", ["id"], unique=False)
    op.create_index(op.f("ix_refresh_token_sessions_token_id"), "refresh_token_sessions", ["token_id"], unique=True)
    op.create_index(op.f("ix_refresh_token_sessions_user_id"), "refresh_token_sessions", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_refresh_token_sessions_user_id"), table_name="refresh_token_sessions")
    op.drop_index(op.f("ix_refresh_token_sessions_token_id"), table_name="refresh_token_sessions")
    op.drop_index(op.f("ix_refresh_token_sessions_id"), table_name="refresh_token_sessions")
    op.drop_index(op.f("ix_refresh_token_sessions_expires_at"), table_name="refresh_token_sessions")
    op.drop_table("refresh_token_sessions")
