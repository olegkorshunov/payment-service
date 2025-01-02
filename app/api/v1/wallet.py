from uuid import UUID

from fastapi import APIRouter, Depends, status

import app.services.wallet as wallet_service
from app.dependencies import get_redis_client
from app.models import TransactionScheme, WalletBalanceScheme, WalletCreateScheme

router = APIRouter()


@router.post("/wallet", status_code=status.HTTP_201_CREATED)
async def create_wallet(wallet: WalletCreateScheme) -> WalletBalanceScheme:
    return await wallet_service.create_wallet(wallet)


@router.get("/wallet/{uuid}", status_code=status.HTTP_200_OK)
async def get_wallet_balance_by_wallet_id(uuid: UUID, redis=Depends(get_redis_client)) -> WalletBalanceScheme:
    return await wallet_service.get_wallet_balance_by_wallet_id(uuid, redis)


@router.get("/users/{uuid}/wallet", status_code=status.HTTP_200_OK)
async def get_wallet_balance_by_user_id(uuid: UUID) -> list[WalletBalanceScheme]:
    return await wallet_service.get_wallet_balance_by_user_id(uuid)


@router.post("/wallet/transaction", status_code=status.HTTP_200_OK)
async def create_transaction(uuid: UUID, transaction: TransactionScheme) -> TransactionScheme:
    # TODO: user_id from jwt
    return await wallet_service.create_transaction(uuid, transaction)
