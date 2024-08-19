from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Set


class UserSchemaAdd(BaseModel):
    """
    Схема модели User, используется при создании
    """
    username: str = Field(min_length=5, max_length=30, pattern="^[A-Za-z0-9-_]+$")
    password: str = Field(min_length=5)

    model_config = ConfigDict(from_attributes=True)

class UserSchema(BaseModel):
    """
    Общая схема модели User
    """
    id: int
    username: str
    hashed_password: str
    created_at: datetime
    updated_at: datetime
    posts: Set

    model_config = ConfigDict(from_attributes=True)

class UserSchemaUpdate(BaseModel):
    """
    Схема модели User, используется при обновлении
    """
    username: str = Field(min_length=5, max_length=30, pattern="^[A-Za-z0-9-_]+$")
    password: str = Field(min_length=5)



