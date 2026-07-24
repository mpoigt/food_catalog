from core.exceptions.base import BaseAppException


class UserNotFoundError(BaseAppException):
    message = "User not found"


class UserAlreadyExistsError(BaseAppException):
    message = "User already exists"


class InvalidPasswordError(BaseAppException):
    message = "Invalid password"


class InvalidTokenError(BaseAppException):
    message = "Invalid or expired token"


class UserBlockedError(BaseAppException):
    message = "User is blocked"


class AccessDeniedError(BaseAppException):
    message = "Access denied"


class SelfActionForbiddenError(BaseAppException):
    message = "You cannot block, delete or change the role of your own account"
