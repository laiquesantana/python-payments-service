"""create category

Revision ID: 65144b5fd377
Revises: 040efe510930
Create Date: 2023-05-03 10:15:41.178475

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "65144b5fd377"
down_revision = ""
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "categories",
        sa.Column("guid", sa.String(36), primary_key=True),
        sa.Column("name", sa.String(), index=True, nullable=False),
        sa.Column("description", sa.String(), index=True, nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("updated_at", sa.DateTime, nullable=False),
        sa.Column("deleted_at", sa.DateTime),
    )

    op.create_unique_constraint("unique_categories_name", "categories", ["name"])
    op.create_check_constraint(
        constraint_name="check_categories_timestamps_consistency",
        table_name="categories",
        condition="(created_at <= updated_at) AND (updated_at <= deleted_at)",
    )


def downgrade() -> None:
    op.drop_constraint(
        constraint_name="check_categories_timestamps_consistency",
        table_name="categories",
        type_="check",
    )
    op.drop_constraint(
        constraint_name="unique_categories_name",
        table_name="categories",
        type_="unique",
    )
    op.drop_table("categories")
