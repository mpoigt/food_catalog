from fastapi import FastAPI

from infrastructure.logging_config import setup_logging
from presentation.api.exceptions.exception_handlers import init_exceptions_handlers
from presentation.api.routers.auth import router as auth_router
from presentation.api.routers.token import router as token_router
from presentation.api.routers.user import router as user_router
from presentation.dependencies.container import container

setup_logging()

container.wire(
    modules=[
        "presentation.api.routers.auth",
        "presentation.api.routers.token",
        "presentation.api.routers.user",
        "presentation.dependencies.auth",
    ]
)

app = FastAPI(title="Каталог продуктов — Auth")

init_exceptions_handlers(app)

app.include_router(auth_router)
app.include_router(token_router)
app.include_router(user_router)
