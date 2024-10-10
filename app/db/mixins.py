from datetime import UTC, datetime

from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column


class CreatedMixin(object):
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))


class UpdatedMixin(object):
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=lambda: datetime.now(UTC),
    )


class TimestampMixin(CreatedMixin, UpdatedMixin):
    pass
