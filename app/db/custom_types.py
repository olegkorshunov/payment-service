import uuid
from typing import Annotated

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column

UUID_PK = Annotated[uuid.UUID, mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)]
