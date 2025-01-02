from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.tools.pydantic import MONEY_DECIMAL


class BasePydanticModel(BaseModel):
    class Config:
        orm_mode = True


class WalletBalanceScheme(BasePydanticModel):
    id: UUID
    user_id: UUID
    balance: MONEY_DECIMAL
    name: str

    def dict(self, **kwargs):
        data = super().dict(**kwargs)
        data["id"] = str(self.id)
        data["user_id"] = str(self.user_id)
        data["balance"] = str(self.balance)
        return data


class WalletCreateScheme(BasePydanticModel):
    user_id: UUID
    name: str


class TransactionScheme(BasePydanticModel):
    wallet_out_id: UUID
    wallet_in_id: UUID
    amount: MONEY_DECIMAL
    created_at: datetime
