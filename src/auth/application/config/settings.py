from abc import ABC, abstractmethod


class SettingsServiceABC(ABC):
    @property
    @abstractmethod
    def access_token_expire(self) -> int: ...

    @property
    @abstractmethod
    def refresh_token_expire(self) -> int: ...
