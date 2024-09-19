from sqlalchemy.ext.asyncio import AsyncSession

from models.users import User
from schemas.posts import PostSchema, PostSchemaAdd, PostSchemaUpdate
from utils.repository import AbstractRepository


class PostsService:
    def __init__(self, posts_repo: AbstractRepository):
        self.posts_repo: AbstractRepository = posts_repo()

    async def add_post(self, session: AsyncSession, user: User, post: PostSchemaAdd):
        p_dict = post.model_dump()
        p_dict.update({"user_id": user.id})
        p_id = await self.posts_repo.add_one(session, p_dict)
        await session.commit()
        return p_id

    async def get_post(self, session: AsyncSession, **filters) -> PostSchema:
        post = await self.posts_repo.get_one(session, **filters)
        return post

    async def get_posts(self, session: AsyncSession, **filters) -> list[PostSchema]:
        posts = await self.posts_repo.get_all(session, **filters)
        return posts

    async def update_post(self, session: AsyncSession, post: PostSchemaUpdate, **ids):
        p_dict = post.model_dump()
        p_id = await self.posts_repo.update_one(session, p_dict, **ids)
        await session.commit()
        return p_id

    async def delete_post(self, session: AsyncSession, **ids):
        p_id = await self.posts_repo.delete_one(session, **ids)
        await session.commit()
        return p_id
