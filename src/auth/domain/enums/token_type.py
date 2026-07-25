from enum import Enum

TOKEN_TYPE_CLAIM = "token_type"


class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"
