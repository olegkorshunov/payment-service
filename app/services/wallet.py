import uuid

from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from redis.asyncio import Redis
from sqlalchemy import select

from app.db import Wallet
from app.db.registry import ASYNC_SESSION_MAKER
from app.models import WalletBalanceScheme, WalletCreateScheme


async def get_wallet_balance_by_wallet_id(wallet_id: uuid.UUID, redis: Redis):
    wallet_key = f"wallet:{wallet_id}"
    if wallet_from_redis := await redis.hgetall(wallet_key):
        return jsonable_encoder(wallet_from_redis.items())
    else:
        async with ASYNC_SESSION_MAKER() as session:
            wallet = await session.get(Wallet, wallet_id)

            if not wallet:
                raise HTTPException(status_code=404)
            await redis.hset(wallet_key, mapping=WalletBalanceScheme.from_orm(wallet).dict())
            await redis.expire(wallet_key, 60 * 10)
            return wallet


async def get_wallet_balance_by_user_id(user_id: uuid.UUID):
    async with ASYNC_SESSION_MAKER() as session:
        query = select(Wallet).where(Wallet.user_id == user_id)
        result = await session.execute(query)
        wallets = result.scalars().all()
        if not wallets:
            raise HTTPException(status_code=404)
        return wallets


async def create_wallet(wallet_data: WalletCreateScheme):
    async with ASYNC_SESSION_MAKER() as session:
        wallet = Wallet(**wallet_data.dict())
        session.add(wallet)
        await session.commit()
        return wallet
