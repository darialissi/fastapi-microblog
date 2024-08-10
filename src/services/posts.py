from schemas.posts import PostSchemaAdd, PostSchema, PostSchemaUpdate
from utils.repository import AbstractRepository


class PostsService:
    def __init__(self, posts_repo: AbstractRepository):
        self.posts_repo: AbstractRepository = posts_repo()

    async def add_post(self, post: PostSchemaAdd) -> dict:
        post_id = await self.posts_repo.add_one(post)
        return post_id

    async def get_post(self, **filters) -> list[PostSchema]:
        post = await self.posts_repo.get_one(**filters)
        return post

    async def get_posts(self, **filters) -> list[PostSchema]:
        posts = await self.posts_repo.get_all(**filters)
        return posts

    async def update_post(self, data: PostSchemaUpdate, **ids) -> dict:
        response = await self.posts_repo.update_one(data, **ids)
        return response

    async def delete_post(self, **ids) -> dict:
        response = await self.posts_repo.delete_one(**ids)
        return response