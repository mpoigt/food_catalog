from fastapi import status

from application.exceptions.base_exception import BaseAppException
from application.exceptions.user_exception import (
    AccessDeniedError,
    InvalidPasswordError,
    InvalidTokenError,
    UserAlreadyExistsError,
    UserBlockedError,
    UserNotFoundError,
)

EXCEPTION_STATUS_MAP: dict[type[BaseAppException], int] = {
    UserNotFoundError: status.HTTP_404_NOT_FOUND,
    UserAlreadyExistsError: status.HTTP_409_CONFLICT,
    InvalidPasswordError: status.HTTP_401_UNAUTHORIZED,
    InvalidTokenError: status.HTTP_401_UNAUTHORIZED,
    UserBlockedError: status.HTTP_403_FORBIDDEN,
    AccessDeniedError: status.HTTP_403_FORBIDDEN,
}
