from sqlalchemy.ext.asyncio import AsyncSession

from models.users import User
from schemas.comments import CommentSchema, CommentSchemaAdd, CommentSchemaUpdate
from utils.repository import AbstractRepository


class CommentsService:
    def __init__(self, comments_repo: AbstractRepository):
        self.comments_repo: AbstractRepository = comments_repo()

    async def add_comment(self, session: AsyncSession, user: User, comment: CommentSchemaAdd, **ids):
        c_dict = comment.model_dump()
        c_dict.update({"author_id": user.id})
        c_id = await self.comments_repo.add_one(session, c_dict, **ids)
        await session.commit()
        return c_id

    async def get_comment(self, session: AsyncSession, **filters) -> CommentSchema:
        comment = await self.comments_repo.get_one(session, **filters)
        return comment

    async def get_comments(self, session: AsyncSession, **filters) -> list[CommentSchema]:
        comments = await self.comments_repo.get_all(session, **filters)
        return comments

    async def update_comment(self, session: AsyncSession, comment: CommentSchemaUpdate, **ids):
        c_dict = comment.model_dump()
        c_id = await self.comments_repo.update_one(session, c_dict, **ids)
        await session.commit()
        return c_id

    async def delete_comment(self, session: AsyncSession, **ids):
        c_id = await self.comments_repo.delete_one(session, **ids)
        await session.commit()
        return c_id
