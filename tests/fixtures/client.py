import asyncio
from asyncio import AbstractEventLoop
from typing import AsyncGenerator, Generator

import pytest
from httpx import AsyncClient

from app.main import app


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as _client:
        await app.router.startup()
        yield _client
        await app.router.shutdown()
