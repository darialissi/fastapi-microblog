from schemas.posts import PostSchemaAdd, PostSchema, PostSchemaUpdate
from utils.unitofwork import IUnitOfWork


class PostsService:

    async def add_post(self, uow: IUnitOfWork, post: PostSchemaAdd):
        async with uow:
            p_id = await uow.posts.add_one(post)
            await uow.commit()
        return p_id

    async def get_post(self, uow: IUnitOfWork, **filters) -> PostSchema:
        async with uow:
            post = await uow.posts.get_one(**filters)
            await uow.commit()
        return post

    async def get_posts(self, uow: IUnitOfWork, **filters) -> list[PostSchema]:
        async with uow:
            posts = await uow.posts.get_all(**filters)
            await uow.commit()
        return posts

    async def update_post(self, uow: IUnitOfWork, data: PostSchemaUpdate, **ids):
        async with uow:
            p_id = await uow.posts.update_one(data, **ids)
            await uow.commit()
        return p_id

    async def delete_post(self, uow: IUnitOfWork, **ids):
        async with uow:
            p_id = await uow.posts.delete_one(**ids)
            await uow.commit()
        return p_id