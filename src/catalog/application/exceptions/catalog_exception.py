from core.exceptions.base import BaseAppException


class CategoryNotFoundError(BaseAppException):
    message = "Category not found"


class CategoryAlreadyExistsError(BaseAppException):
    message = "Category already exists"


class ProductNotFoundError(BaseAppException):
    message = "Product not found"


class CurrencyRateUnavailableError(BaseAppException):
    message = "Currency rate is unavailable"


class InvalidImageError(BaseAppException):
    message = "Invalid image file"