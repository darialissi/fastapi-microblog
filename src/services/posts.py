from schemas.posts import PostSchema, PostSchemaAdd, PostSchemaID
from schemas.users import UserSchemaAuth
from utils.unitofwork import DBManager


class PostsService:

    async def add_post(self, db: DBManager, user: UserSchemaAuth, post: PostSchemaAdd) -> PostSchemaID:
        p_dict = post.model_dump()
        p_dict.update({"author_id": user.id})
        p_id = await db.posts.add_one(p_dict)
        await db.commit()
        return PostSchemaID.model_validate({"id": p_id})

    async def get_post(self, db: DBManager, **filters) -> PostSchema:
        if post := await db.posts.get_one(**filters):
            return PostSchema.model_validate(post)

    async def get_posts(self, db: DBManager, **filters) -> list[PostSchema]:
        if posts := await db.posts.get_all(**filters):
            return [PostSchema.model_validate(post) for post in posts]
        return []

    async def is_author_post(self, user_id: int, post_author: int) -> bool:
        return post_author == user_id

    async def update_post(self, db: DBManager, post: PostSchemaAdd, **ids) -> PostSchemaID:
        p_dict = post.model_dump()
        p_id = await db.posts.update_one(p_dict, **ids)
        await db.commit()
        return PostSchemaID.model_validate({"id": p_id})

    async def delete_post(self, db: DBManager, **ids) -> PostSchemaID:
        p_id = await db.posts.delete_one(**ids)
        await db.commit()
        return PostSchemaID.model_validate({"id": p_id})
