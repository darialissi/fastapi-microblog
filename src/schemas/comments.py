from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CommentSchemaAdd(BaseModel):
    """
    Схема модели Comment, используется при создании
    """

    body: str

    model_config = ConfigDict(from_attributes=True)


class CommentSchema(CommentSchemaAdd):
    """
    Общая схема модели Comment
    """

    id: int
    created_at: datetime
    updated_at: datetime

    post_id: int = Field(gt=0)
    author_id: int = Field(gt=0)


class CommentSchemaUpdate(BaseModel):
    """
    Схема модели Comment, используется при обновлении
    """

    body: str
