from schemas.comments import CommentSchemaAdd, CommentSchema, CommentSchemaUpdate
from utils.repository import AbstractRepository


class CommentsService:
    def __init__(self, comments_repo: AbstractRepository):
        self.comments_repo: AbstractRepository = comments_repo()

    async def add_comment(self, comment: CommentSchemaAdd, **ids):
        c_id = await self.comments_repo.add_one(comment, **ids)
        return c_id

    async def get_comment(self, **filters) -> CommentSchema:
        comment = await self.comments_repo.get_one(**filters)
        return comment

    async def get_comments(self, **filters) -> list[CommentSchema]:
        comments = await self.comments_repo.get_all(**filters)
        return comments

    async def update_comment(self, data: CommentSchemaUpdate, **ids):
        c_id = await self.comments_repo.update_one(data, **ids)
        return c_id

    async def delete_comment(self, **ids):
        c_id = await self.comments_repo.delete_one(**ids)
        return c_id