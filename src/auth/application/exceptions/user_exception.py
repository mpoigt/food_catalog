from application.exceptions.base_exception import BaseAppException


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
