"""Initial tables

Revision ID: 43423a6fd434
Revises:
Create Date: 2026-06-25 17:52:31.055032

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "43423a6fd434"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "departments",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("name", sa.String, nullable=False, unique=True),
    )

    op.create_table(
        "employees",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("username", sa.String, nullable=False, unique=True),
        sa.Column("email", sa.String, nullable=False, unique=True),
        sa.Column("full_name", sa.String, nullable=False),
        sa.Column("password_hash", sa.String, nullable=False),
        sa.Column("department_id", sa.Integer, nullable=False),
        sa.ForeignKeyConstraint(["department_id"], ["departments.id"]),
    )

    op.create_index(op.f("ix_employees_username"), "employees", ["username"], unique=True)
    op.create_index(op.f("ix_employees_email"), "employees", ["email"], unique=True)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("employees")
    op.drop_table("departments")
