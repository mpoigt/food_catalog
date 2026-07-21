from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, status

from application.use_cases.token.refreshing import RefreshJWTTokensUseCase
from presentation.api.schemas.token_pair import TokenPairSchema
from presentation.dependencies.container import Container

router = APIRouter(prefix="/tokens", tags=["Tokens"])


@router.post("/refresh", response_model=TokenPairSchema, status_code=status.HTTP_200_OK)
@inject
async def refresh(
    refresh_token: str = Body(..., embed=True, alias="refreshToken"),
    use_case: RefreshJWTTokensUseCase = Depends(
        Provide[Container.refresh_tokens_use_case]
    ),
) -> TokenPairSchema:
    tokens = await use_case(refresh_token)
    return TokenPairSchema(
        access_token=tokens.access_token, refresh_token=tokens.refresh_token
    )
