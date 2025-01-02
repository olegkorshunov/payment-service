import uuid

from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from redis.asyncio import Redis
from sqlalchemy import insert, select

from app.db import Transaction, Wallet
from app.db.registry import ASYNC_SESSION_MAKER
from app.models import TransactionScheme, WalletBalanceScheme, WalletCreateScheme


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


async def create_transaction(user_ud: uuid.UUID, transaction_data: TransactionScheme):
    async with ASYNC_SESSION_MAKER() as session:
        wallet_out_q = select(Wallet).where(Wallet.id == transaction_data.wallet_out_id).with_for_update()
        wallet_in_q = select(Wallet).where(Wallet.id == transaction_data.wallet_in_id).with_for_update()
        wallet_out = await session.execute(wallet_out_q)
        wallet_in = await session.execute(wallet_in_q)
        wallet_out = wallet_out.scalars().one_or_none()
        wallet_in = wallet_in.scalars().one_or_none()
        if not wallet_out or not wallet_in:
            raise HTTPException(status_code=404)
        if wallet_out.balance < transaction_data.amount:
            raise HTTPException(status_code=400)

        wallet_out.balance -= transaction_data.amount
        wallet_in.balance += transaction_data.amount
        transaction = insert(Transaction).values(
            user_id=user_ud,
            amount=transaction_data.amount,
            sender_wallet_id=transaction_data.wallet_out_id,
            receiver_wallet_id=transaction_data.wallet_in_id,
        )
        session.add(transaction)
        await session.commit()
        return transaction
