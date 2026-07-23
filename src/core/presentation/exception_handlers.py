import logging

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from core.exceptions.base import BaseAppException

logger = logging.getLogger("api")

ExceptionStatusMap = dict[type[BaseAppException], int]


def init_exception_handlers(app: FastAPI, status_map: ExceptionStatusMap) -> None:
    @app.exception_handler(BaseAppException)
    async def handle_app_exception(
        request: Request, exc: BaseAppException
    ) -> JSONResponse:
        status_code = status_map.get(type(exc), status.HTTP_400_BAD_REQUEST)
        logger.warning(
            "app_exception",
            extra={
                "error": type(exc).__name__,
                "detail": exc.detail,
                "path": request.url.path,
            },
        )
        content: dict[str, str] = {"message": exc.message}
        if exc.detail:
            content["detail"] = exc.detail
        return JSONResponse(status_code=status_code, content=content)

    @app.exception_handler(Exception)
    async def handle_unexpected(request: Request, exc: Exception) -> JSONResponse:
        logger.error(
            "unhandled_exception",
            exc_info=exc,
            extra={"path": request.url.path},
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Internal server error"},
        )