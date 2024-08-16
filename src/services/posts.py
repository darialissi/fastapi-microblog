from schemas.posts import PostSchemaAdd, PostSchema, PostSchemaUpdate
from utils.repository import AbstractRepository
from sqlalchemy.ext.asyncio import AsyncSession


class PostsService:
    def __init__(self, posts_repo: AbstractRepository):
        self.posts_repo: AbstractRepository = posts_repo()

    async def add_post(self, session: AsyncSession, post: PostSchemaAdd):
        p_id = await self.posts_repo.add_one(session, post)
        return p_id

    async def get_post(self, session: AsyncSession, **filters) -> PostSchema:
        post = await self.posts_repo.get_one(session, **filters)
        return post

    async def get_posts(self, session: AsyncSession, **filters) -> list[PostSchema]:
        posts = await self.posts_repo.get_all(session, **filters)
        return posts

    async def update_post(self, session: AsyncSession, data: PostSchemaUpdate, **ids):
        p_id = await self.posts_repo.update_one(session, data, **ids)
        return p_id

    async def delete_post(self, session: AsyncSession, **ids):
        p_id = await self.posts_repo.delete_one(session, **ids)
        return p_id