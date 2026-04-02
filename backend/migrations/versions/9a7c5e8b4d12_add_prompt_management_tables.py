"""add prompt management tables

Revision ID: 9a7c5e8b4d12
Revises: 4c1f7a9d2b61
Create Date: 2026-04-01 11:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "9a7c5e8b4d12"
down_revision: Union[str, None] = "4c1f7a9d2b61"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "prompts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=80), nullable=False),
        sa.Column("version", sa.String(length=20), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name", "version", name="uq_prompts_name_version"),
    )
    op.create_index(op.f("ix_prompts_id"), "prompts", ["id"], unique=False)
    op.create_index(op.f("ix_prompts_name"), "prompts", ["name"], unique=False)
    op.create_index(op.f("ix_prompts_version"), "prompts", ["version"], unique=False)

    op.create_table(
        "ai_prompt_runs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("operation", sa.String(length=50), nullable=False),
        sa.Column("prompt_name", sa.String(length=80), nullable=False),
        sa.Column("prompt_version", sa.String(length=20), nullable=False),
        sa.Column("context_json", sa.Text(), nullable=False),
        sa.Column("response_json", sa.Text(), nullable=False),
        sa.Column("latency_ms", sa.Integer(), server_default=sa.text("0"), nullable=False),
        sa.Column("retries", sa.Integer(), server_default=sa.text("0"), nullable=False),
        sa.Column("error_text", sa.Text(), server_default=sa.text("''"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_ai_prompt_runs_id"), "ai_prompt_runs", ["id"], unique=False)
    op.create_index(op.f("ix_ai_prompt_runs_operation"), "ai_prompt_runs", ["operation"], unique=False)
    op.create_index(op.f("ix_ai_prompt_runs_prompt_name"), "ai_prompt_runs", ["prompt_name"], unique=False)
    op.create_index(op.f("ix_ai_prompt_runs_prompt_version"), "ai_prompt_runs", ["prompt_version"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_ai_prompt_runs_prompt_version"), table_name="ai_prompt_runs")
    op.drop_index(op.f("ix_ai_prompt_runs_prompt_name"), table_name="ai_prompt_runs")
    op.drop_index(op.f("ix_ai_prompt_runs_operation"), table_name="ai_prompt_runs")
    op.drop_index(op.f("ix_ai_prompt_runs_id"), table_name="ai_prompt_runs")
    op.drop_table("ai_prompt_runs")

    op.drop_index(op.f("ix_prompts_version"), table_name="prompts")
    op.drop_index(op.f("ix_prompts_name"), table_name="prompts")
    op.drop_index(op.f("ix_prompts_id"), table_name="prompts")
    op.drop_table("prompts")
