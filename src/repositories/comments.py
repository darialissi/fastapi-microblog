from models.comments import Comments
from utils.repository import SQLAlchemyRepository


class CommentsRepository(SQLAlchemyRepository):
    model = Comments