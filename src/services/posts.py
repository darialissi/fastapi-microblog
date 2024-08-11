from schemas.posts import PostSchemaAdd, PostSchema, PostSchemaUpdate
from utils.repository import AbstractRepository


class PostsService:
    def __init__(self, posts_repo: AbstractRepository):
        self.posts_repo: AbstractRepository = posts_repo()

    async def add_post(self, post: PostSchemaAdd):
        p_id = await self.posts_repo.add_one(post)
        return p_id

    async def get_post(self, **filters) -> PostSchema:
        post = await self.posts_repo.get_one(**filters)
        return post

    async def get_posts(self, **filters) -> list[PostSchema]:
        posts = await self.posts_repo.get_all(**filters)
        return posts

    async def update_post(self, data: PostSchemaUpdate, **ids):
        p_id = await self.posts_repo.update_one(data, **ids)
        return p_id

    async def delete_post(self, **ids):
        p_id = await self.posts_repo.delete_one(**ids)
        return p_id