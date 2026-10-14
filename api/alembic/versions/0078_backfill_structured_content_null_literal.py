"""Backfill structured_content JSON null literal to SQL NULL.

Revision ID: 0078
Revises: 0077

Before ADR 0026, the Docling integration stored a Python ``None`` in
``documents.structured_content`` without ``none_as_null=True`` on the
SQLAlchemy column. SQLAlchemy's JSONB type serialises ``None`` as the
JSON ``'null'`` literal rather than SQL NULL, so rows where Docling
produced no output carry the JSON string ``'null'`` instead of a true
NULL. This breaks any future ``WHERE structured_content IS NOT NULL``
predicate, which would match those rows incorrectly.

ADR 0026 adds ``none_as_null=True`` to the column definition. This
migration backfills the existing rows so the invariant holds across
old and new ingestions.

Downgrade is a no-op — converting the JSON literal back would be
indistinguishable from a document that genuinely stored the JSON value
``null``, and no application code reads the distinction.
"""

from alembic import op

revision = "0078"
down_revision = "0077"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        "UPDATE documents SET structured_content = NULL "
        "WHERE structured_content = 'null'::jsonb"
    )


def downgrade() -> None:
    pass
