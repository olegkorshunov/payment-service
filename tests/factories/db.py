import uuid

import factory.fuzzy

from app import db
from app.db.registry import ASYNC_SESSION_MAKER
from tests.utils import AsyncSQLAlchemyFactory


class WalletModelFactory(AsyncSQLAlchemyFactory):
    id = factory.LazyFunction(uuid.uuid4)
    user_id = factory.LazyFunction(uuid.uuid4)
    name = factory.Faker("pystr", min_chars=1, max_chars=128)

    class Meta:
        # pylint: disable=unnecessary-lambda-assignment
        model = db.Wallet
        async_alchemy_get_or_create = ("id",)
        async_alchemy_session_factory = lambda: ASYNC_SESSION_MAKER
