from schemas.comments import CommentSchemaAdd, CommentSchema, CommentSchemaUpdate
from utils.repository import AbstractRepository
from sqlalchemy.ext.asyncio import AsyncSession


class CommentsService:
    def __init__(self, comments_repo: AbstractRepository):
        self.comments_repo: AbstractRepository = comments_repo()

    async def add_comment(self, session: AsyncSession, comment: CommentSchemaAdd, **ids):
        c_id = await self.comments_repo.add_one(session, comment, **ids)
        return c_id

    async def get_comment(self, session: AsyncSession, **filters) -> CommentSchema:
        comment = await self.comments_repo.get_one(session, **filters)
        return comment

    async def get_comments(self, session: AsyncSession, **filters) -> list[CommentSchema]:
        comments = await self.comments_repo.get_all(session, **filters)
        return comments

    async def update_comment(self, session: AsyncSession, data: CommentSchemaUpdate, **ids):
        c_id = await self.comments_repo.update_one(session, data, **ids)
        return c_id

    async def delete_comment(self, session: AsyncSession, **ids):
        c_id = await self.comments_repo.delete_one(session, **ids)
        return c_id