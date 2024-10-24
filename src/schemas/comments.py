from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CommentSchemaAdd(BaseModel):
    """
    Схема модели Comment, используется при создании/обновлении
    """

    body: str

    model_config = ConfigDict(from_attributes=True)


class CommentSchemaID(BaseModel):
    """
    Схема модели Comment ID
    """

    id: int


class CommentSchema(CommentSchemaAdd, CommentSchemaID):
    """
    Общая схема модели Comment
    """

    created_at: datetime
    updated_at: datetime

    post_id: int = Field(gt=0)
    author_id: int = Field(gt=0)
