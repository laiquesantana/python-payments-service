"""insert categories

Revision ID: 79bbcd606c6d
Revises: 61aedd14b372
Create Date: 2023-05-08 12:58:58.326831

"""

from datetime import datetime
from uuid import uuid4

from alembic import op
from sqlalchemy import MetaData, Table

# revision identifiers, used by Alembic.
revision = "79bbcd606c6d"
down_revision = "65144b5fd377"
branch_labels = None
depends_on = None


def data_categories() -> list[dict[str, str]]:
    return [
        {
            "name": "input_certifix",
            "description": "Arquivo de entrada do Certifix. Utilizado ",
        },
    ]


def upgrade() -> None:
    rows = []
    categories = data_categories()
    for category in categories:
        datetime_now = datetime.now()
        category.update(
            {
                "guid": str(uuid4()),
                "created_at": datetime_now,
                "updated_at": datetime_now,
            }
        )
        rows.append(category)

    metadata = MetaData()
    metadata.reflect(only=("categories",), bind=op.get_bind())
    categories_table: Table = Table("categories", metadata)
    op.bulk_insert(categories_table, rows)


def downgrade() -> None:
    categories = data_categories()
    for category in categories:
        op.execute(f"DELETE FROM categories where name = '{category['name']}'")
