class BaseAppException(Exception):
    message: str = "Error"

    def __init__(self, detail: str | None = None):
        self.detail = detail
        super().__init__(detail or self.message)
