import uuid

import factory.fuzzy

from app.models import WalletCreateScheme


class WalletSchemeFactory(factory.Factory):
    user_id = factory.LazyFunction(uuid.uuid4)
    name = factory.Faker("pystr", min_chars=1, max_chars=128)

    class Meta:
        model = WalletCreateScheme
