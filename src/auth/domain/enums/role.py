from enum import Enum


class Role(str, Enum):
    USER = "user"
    ADVANCED = "advanced"
    ADMIN = "admin"
