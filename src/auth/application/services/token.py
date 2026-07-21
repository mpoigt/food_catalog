from abc import ABC, abstractmethod


class TokenServiceJWTABC(ABC):
    @abstractmethod
    def generate_token(self, data: dict, expires: int) -> str: ...

    @abstractmethod
    def decode_token(self, token: str) -> dict: ...
