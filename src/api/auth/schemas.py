from enum import StrEnum, auto

from pydantic import BaseModel


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


class TokenType(StrEnum):
    access = auto()
    refresh = auto()
