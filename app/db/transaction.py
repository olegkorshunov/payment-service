from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import DECIMAL, CheckConstraint, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.custom_types import UUID_PK
from app.db.mixins import TimestampMixin
from app.db.registry import Base

if TYPE_CHECKING:
    from app.db import TransactionEvent, Wallet


class Transaction(Base, TimestampMixin):
    __tablename__ = "transaction"
    id: Mapped[UUID_PK]
    user_id: Mapped[UUID] = mapped_column(nullable=False)
    amount: Mapped[DECIMAL] = mapped_column(DECIMAL(precision=10, scale=2), nullable=False)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)

    sender_wallet_id: Mapped[UUID] = mapped_column(ForeignKey("wallet.id"), nullable=False)
    sender_wallet: Mapped["Wallet"] = relationship(
        "Wallet", foreign_keys=[sender_wallet_id], back_populates="sent_transactions"
    )
    receiver_wallet_id: Mapped[UUID] = mapped_column(ForeignKey("wallet.id"), nullable=False)
    receiver_wallet: Mapped["Wallet"] = relationship(
        "Wallet", foreign_keys=[receiver_wallet_id], back_populates="received_transactions"
    )
    event: Mapped["TransactionEvent"] = relationship("TransactionEvent", back_populates="transaction")

    __table_args__ = (
        CheckConstraint("amount >= 0", name="check_transaction_amount_non_negative"),
        Index("transaction_idx_user_id", "user_id"),
    )
