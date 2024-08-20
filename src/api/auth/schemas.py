from pydantic import BaseModel
from enum import StrEnum, auto


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"

class TokenType(StrEnum):
    access = auto()
    refresh = auto()