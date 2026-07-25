from fastapi import status

from catalog.application.exceptions.catalog_exception import (
    CategoryAlreadyExistsError,
    CategoryNotFoundError,
    CurrencyRateUnavailableError,
    InvalidImageError,
    ProductNotFoundError,
)
from core.exceptions.base import BaseAppException

EXCEPTION_STATUS_MAP: dict[type[BaseAppException], int] = {
    CategoryNotFoundError: status.HTTP_404_NOT_FOUND,
    CategoryAlreadyExistsError: status.HTTP_409_CONFLICT,
    ProductNotFoundError: status.HTTP_404_NOT_FOUND,
    CurrencyRateUnavailableError: status.HTTP_503_SERVICE_UNAVAILABLE,
    InvalidImageError: status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
}