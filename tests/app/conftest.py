from typing import AsyncGenerator

import pytest
from sqlalchemy.sql import text

from app import db
from app.db.registry import ASYNC_SESSION_MAKER

TRUNCATE_QUERY = "TRUNCATE TABLE {tbl_name} CASCADE;"


@pytest.fixture
async def clear_db() -> AsyncGenerator[None, None]:
    yield
    async with ASYNC_SESSION_MAKER() as session:
        # TODO:
        await session.commit()
