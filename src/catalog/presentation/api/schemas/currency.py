from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class UsdRateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    rate: Decimal
    date: str
