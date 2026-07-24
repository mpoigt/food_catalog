from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from auth.presentation.api.exceptions.constants import (
    EXCEPTION_STATUS_MAP as AUTH_EXCEPTIONS,
)
from auth.presentation.api.routers.auth import router as auth_router
from auth.presentation.api.routers.token import router as token_router
from auth.presentation.api.routers.user import router as user_router
from auth.presentation.dependencies.container import (
    AUTH_WIRING_MODULES,
)
from auth.presentation.dependencies.container import (
    container as auth_container,
)
from catalog.presentation.api.exceptions.constants import (
    EXCEPTION_STATUS_MAP as CATALOG_EXCEPTIONS,
)
from catalog.presentation.api.routers.category import router as category_router
from catalog.presentation.api.routers.currency import router as currency_router
from catalog.presentation.api.routers.product import router as product_router
from catalog.presentation.dependencies.container import (
    CATALOG_WIRING_MODULES,
)
from catalog.presentation.dependencies.container import (
    container as catalog_container,
)
from core.container import CoreContainer
from core.logging.config import setup_logging
from core.presentation.exception_handlers import init_exception_handlers

setup_logging()

core_container = CoreContainer()
auth_container.session_factory.override(core_container.session_factory)
auth_container.wire(modules=AUTH_WIRING_MODULES)
catalog_container.session_factory.override(core_container.session_factory)
catalog_container.wire(modules=CATALOG_WIRING_MODULES)

app = FastAPI(title="Каталог продуктов")

init_exception_handlers(app, {**AUTH_EXCEPTIONS, **CATALOG_EXCEPTIONS})

app.include_router(auth_router)
app.include_router(token_router)
app.include_router(user_router)
app.include_router(category_router)
app.include_router(product_router)
app.include_router(currency_router)

media_settings = catalog_container.media_settings()
Path(media_settings.media_root).mkdir(parents=True, exist_ok=True)
app.mount(
    media_settings.media_url,
    StaticFiles(directory=media_settings.media_root),
    name="media",
)