from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from auth.presentation.dependencies.auth import get_current_user
from catalog.application.use_cases.currency.get_usd_rate import GetUsdRateUseCase
from catalog.presentation.api.schemas.currency import UsdRateSchema
from catalog.presentation.dependencies.container import CatalogContainer

router = APIRouter(
    prefix="/currency",
    tags=["Currency"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/usd-rate", response_model=UsdRateSchema)
@inject
async def get_usd_rate(
    use_case: GetUsdRateUseCase = Depends(
        Provide[CatalogContainer.get_usd_rate_use_case]
    ),
) -> UsdRateSchema:
    rate = await use_case()
    return UsdRateSchema.model_validate(rate)
