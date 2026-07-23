from dependency_injector import containers, providers
from redis.asyncio import Redis  # type: ignore[import-untyped]

from core.config.settings import RedisSettings

from catalog.application.use_cases.category.create_category import CreateCategoryUseCase
from catalog.application.use_cases.category.delete_category import DeleteCategoryUseCase
from catalog.application.use_cases.category.get_category import GetCategoryUseCase
from catalog.application.use_cases.category.list_categories import ListCategoriesUseCase
from catalog.application.use_cases.category.update_category import UpdateCategoryUseCase
from catalog.application.use_cases.currency.get_product_price_usd import (
    GetProductPriceUsdUseCase,
)
from catalog.application.use_cases.product.create_product import CreateProductUseCase
from catalog.application.use_cases.product.delete_product import DeleteProductUseCase
from catalog.application.use_cases.product.get_product import GetProductUseCase
from catalog.application.use_cases.product.list_products import ListProductsUseCase
from catalog.application.use_cases.product.update_product import UpdateProductUseCase
from catalog.infrastructure.db.uow.uow import CatalogUnitOfWork
from catalog.infrastructure.services.currency import NBRBCurrencyService


class CatalogContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "catalog.presentation.api.routers.category",
            "catalog.presentation.api.routers.product",
        ],
    )

    session_factory = providers.Dependency()

    redis_settings = providers.Singleton(RedisSettings)
    redis_client = providers.Singleton(
        Redis,
        host=redis_settings.provided.host,
        port=redis_settings.provided.port,
        db=redis_settings.provided.db,
    )

    uow = providers.Factory(CatalogUnitOfWork, session_factory=session_factory)
    currency_service = providers.Factory(NBRBCurrencyService, redis=redis_client)

    create_category_use_case = providers.Factory(CreateCategoryUseCase, uow=uow)
    update_category_use_case = providers.Factory(UpdateCategoryUseCase, uow=uow)
    delete_category_use_case = providers.Factory(DeleteCategoryUseCase, uow=uow)
    get_category_use_case = providers.Factory(GetCategoryUseCase, uow=uow)
    list_categories_use_case = providers.Factory(ListCategoriesUseCase, uow=uow)

    create_product_use_case = providers.Factory(CreateProductUseCase, uow=uow)
    update_product_use_case = providers.Factory(UpdateProductUseCase, uow=uow)
    delete_product_use_case = providers.Factory(DeleteProductUseCase, uow=uow)
    get_product_use_case = providers.Factory(GetProductUseCase, uow=uow)
    list_products_use_case = providers.Factory(ListProductsUseCase, uow=uow)

    get_product_price_usd_use_case = providers.Factory(
        GetProductPriceUsdUseCase, uow=uow, currency_service=currency_service
    )


container = CatalogContainer()