"""02_event_table

Revision ID: 780c1d7c2093
Revises: 53d06bc95d63
Create Date: 2025-01-04 23:24:28.529467

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "780c1d7c2093"
down_revision = "53d06bc95d63"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    sa.Enum("NEW", "FAIL", "SUCCESS", name="eventstatus").create(op.get_bind())
    op.create_table(
        "transaction_event",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "status",
            postgresql.ENUM("NEW", "FAIL", "SUCCESS", name="eventstatus", create_type=False),
            nullable=False,
        ),
        sa.Column("body", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("transaction_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["transaction_id"],
            ["transaction.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("transaction_event")
    sa.Enum("NEW", "FAIL", "SUCCESS", name="eventstatus").drop(op.get_bind())
    # ### end Alembic commands ###