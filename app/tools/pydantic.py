from decimal import Decimal
from typing import Annotated

from pydantic import Field

MONEY_DECIMAL_PLACES = 2
MONEY_GE = 0
MAX_DIGITS = 10
MONEY_EXAMPLE = Decimal("20.50")


MONEY_DECIMAL = Annotated[
    Decimal, Field(ge=MONEY_GE, max_digits=MAX_DIGITS, decimal_places=MONEY_DECIMAL_PLACES, examples=[MONEY_EXAMPLE])
]
