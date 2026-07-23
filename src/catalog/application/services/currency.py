from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal


@dataclass
class UsdRate:
    rate: Decimal
    date: str


class CurrencyServiceABC(ABC):
    @abstractmethod
    async def get_usd_rate(self) -> UsdRate: ...