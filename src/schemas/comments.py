from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

    
class CommentSchemaAdd(BaseModel):
    """
    Схема модели Comment, используется при создании
    """
    body: str
    author_id: int = Field(gt=0)

    model_config = ConfigDict(from_attributes=True)
    
class CommentSchema(CommentSchemaAdd):
    """
    Общая схема модели Comment
    """
    id: int
    post_id: int = Field(gt=0)
    created_at: datetime
    updated_at: datetime

class CommentSchemaUpdate(BaseModel):
    """
    Схема модели Comment, используется при обновлении
    """
    body: str

