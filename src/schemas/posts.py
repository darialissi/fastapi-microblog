from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from models.categories import Category


class PostSchemaAdd(BaseModel):
    """
    Схема модели Post, используется при создании/обновлении
    """

    title: str
    category: Category
    body: str

    model_config = ConfigDict(use_enum_values=True, from_attributes=True)


class PostSchema(PostSchemaAdd):
    """
    Общая схема модели Post
    """

    id: int
    created_at: datetime
    updated_at: datetime
    author_id: int = Field(gt=0)
