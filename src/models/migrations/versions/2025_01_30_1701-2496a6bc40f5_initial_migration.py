"""initial_migration

Revision ID: 2496a6bc40f5
Revises: 
Create Date: 2025-01-30 17:01:02.946275

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2496a6bc40f5"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "wallet_requests",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("address", sa.String(), nullable=False),
        sa.Column("bandwidth", sa.Float(), nullable=True),
        sa.Column("energy", sa.Float(), nullable=True),
        sa.Column("trx_balance", sa.DECIMAL(), nullable=False),
        sa.Column(
            "timestamp",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_wallet_requests_address"),
        "wallet_requests",
        ["address"],
        unique=False,
    )
    op.create_index(
        op.f("ix_wallet_requests_id"), "wallet_requests", ["id"], unique=False
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_wallet_requests_id"), table_name="wallet_requests")
    op.drop_index(
        op.f("ix_wallet_requests_address"), table_name="wallet_requests"
    )
    op.drop_table("wallet_requests")
    # ### end Alembic commands ###
