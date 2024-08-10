from models.posts import Posts
from utils.repository import SQLAlchemyRepository


class PostsRepository(SQLAlchemyRepository):
    model = Posts