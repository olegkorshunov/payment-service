from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import DECIMAL, VARCHAR, CheckConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.custom_types import UUID_PK
from app.db.mixins import TimestampMixin
from app.db.registry import Base

if TYPE_CHECKING:
    from app.db.transaction import Transaction


class Wallet(Base, TimestampMixin):
    __tablename__ = "wallet"
    id: Mapped[UUID_PK]
    user_id: Mapped[UUID] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(VARCHAR(length=128), nullable=False)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    balance: Mapped[DECIMAL] = mapped_column(DECIMAL(precision=10, scale=2), nullable=False, default=0)

    sent_transactions: Mapped[list["Transaction"]] = relationship(
        "Transaction", foreign_keys="[Transaction.sender_wallet_id]", back_populates="sender_wallet"
    )
    received_transactions: Mapped[list["Transaction"]] = relationship(
        "Transaction", foreign_keys="[Transaction.receiver_wallet_id]", back_populates="receiver_wallet"
    )

    __table_args__ = (
        CheckConstraint("balance >= 0", name="check_wallet_balance_non_negative"),
        CheckConstraint("length(name) >= 1 AND length(name) <= 128", name="check_wallet_name_length"),
        Index("wallet_idx_user_id", "user_id"),
    )
