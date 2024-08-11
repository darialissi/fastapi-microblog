from models.posts import Post
from utils.repository import SQLAlchemyRepository


class PostsRepository(SQLAlchemyRepository):
    model = Post