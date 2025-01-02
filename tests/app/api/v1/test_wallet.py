from typing import TYPE_CHECKING
from uuid import uuid4

import pytest
from fastapi.encoders import jsonable_encoder
from starlette import status

from app.main import app
from tests.factories.db import WalletModelFactory
from tests.factories.schemes import WalletSchemeFactory

if TYPE_CHECKING:
    from httpx import AsyncClient  # type: ignore


@pytest.mark.usefixtures("clear_db")
async def test_functional_wallet(client: "AsyncClient"):
    expected_data = [WalletSchemeFactory.build() for _ in range(3)]
    user_id = uuid4()
    for w in expected_data:
        w.user_id = user_id
        await client.post(
            app.url_path_for(
                "create_wallet",
            ),
            json=jsonable_encoder(w),
        )

    response = await client.get(app.url_path_for("get_wallet_balance_by_user_id", uuid=str(user_id)))
    response_json = response.json()
    assert len(response_json) == 3

    for data in response_json:
        response = await client.get(app.url_path_for("get_wallet_balance_by_wallet_id", uuid=data["id"]))
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == data["id"]


@pytest.mark.usefixtures("clear_db")
async def test_create_wallet(client: "AsyncClient"):
    wallet = WalletSchemeFactory.build()
    response = await client.post(
        app.url_path_for(
            "create_wallet",
        ),
        json=jsonable_encoder(wallet),
    )

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.usefixtures("clear_db")
async def test_get_wallet_balance_by_user_id(client: "AsyncClient"):
    wallet = await WalletModelFactory.create()
    response = await client.get(app.url_path_for("get_wallet_balance_by_user_id", uuid=str(wallet.user_id)))
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0]["id"] == str(wallet.id)


@pytest.mark.usefixtures("clear_db")
async def test_get_wallet_balance_by_wallet_id(client: "AsyncClient"):
    wallet = await WalletModelFactory.create()
    response = await client.get(app.url_path_for("get_wallet_balance_by_wallet_id", uuid=str(wallet.id)))
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == str(wallet.id)
