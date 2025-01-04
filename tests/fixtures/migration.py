from typing import Generator

import pytest
from alembic.command import downgrade, upgrade
from alembic.config import Config as AlembicConfig

from app.config import database as db_config


@pytest.fixture(autouse=True, scope="session")
def migrate_db() -> Generator[None, None, None]:
    if db_config.dsn_host not in ("postgres", "localhost"):
        raise RuntimeError("Migration for tests should be applied only on test DB")

    config = AlembicConfig("alembic.ini")

    upgrade(config, "head")
    yield
    downgrade(config, "base")
