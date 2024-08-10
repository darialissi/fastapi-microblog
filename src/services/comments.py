from schemas.comments import CommentSchemaAdd, CommentSchema, CommentSchemaUpdate
from utils.repository import AbstractRepository


class CommentsService:
    def __init__(self, comments_repo: AbstractRepository):
        self.comments_repo: AbstractRepository = comments_repo()

    async def add_comment(self, comment: CommentSchemaAdd, **ids) -> dict:
        comment_id = await self.comments_repo.add_one(comment, **ids)
        return comment_id

    async def get_comment(self, **filters) -> list[CommentSchema]:
        comment = await self.comments_repo.get_one(**filters)
        return comment

    async def get_comments(self, **filters) -> list[CommentSchema]:
        comments = await self.comments_repo.get_all(**filters)
        return comments

    async def update_comment(self, data: CommentSchemaUpdate, **ids) -> dict:
        response = await self.comments_repo.update_one(data, **ids)
        return response

    async def delete_comment(self, **ids) -> dict:
        response = await self.comments_repo.delete_one(**ids)
        return response