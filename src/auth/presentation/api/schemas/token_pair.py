from pydantic import BaseModel


class TokenPairSchema(BaseModel):
    access_token: str
    refresh_token: str
