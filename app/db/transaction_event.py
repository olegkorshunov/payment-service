from enum import Enum
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Enum as SQLAlchemyEnum

from app.db.custom_types import UUID_PK
from app.db.registry import Base

if TYPE_CHECKING:
    from app.db import Transaction


class EventStatus(str, Enum):
    NEW = "NEW"
    FAIL = "FAIL"
    SUCCESS = "SUCCESS"


class TransactionEvent(Base):
    __tablename__ = "transaction_event"

    id: Mapped[UUID_PK]
    status: Mapped[EventStatus] = mapped_column(SQLAlchemyEnum(EventStatus), default=EventStatus.NEW)
    body: Mapped[dict] = mapped_column(JSONB, nullable=False)

    transaction_id: Mapped[UUID] = mapped_column(ForeignKey("transaction.id"), nullable=False)
    transaction: Mapped["Transaction"] = relationship(
        "Transaction", foreign_keys=[transaction_id], back_populates="event"
    )
