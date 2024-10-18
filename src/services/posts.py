from models.users import User
from schemas.posts import PostSchema, PostSchemaAdd
from schemas.users import UserSchema
from utils.unitofwork import DBManager


class PostsService:

    async def add_post(self, db: DBManager, user: User, post: PostSchemaAdd):
        p_dict = post.model_dump()
        p_dict.update({"author_id": user.id})
        p_id = await db.posts.add_one(p_dict)
        await db.commit()
        return p_id

    async def get_post(self, db: DBManager, **filters) -> PostSchema:
        post = await db.posts.get_one(**filters)
        return post

    async def get_posts(self, db: DBManager, **filters) -> list[PostSchema]:
        posts = await db.posts.get_all(**filters)
        return posts

    async def validate_author_post(self, db: DBManager, user: UserSchema, post_id: int):
        post = await db.posts.get_one(id=post_id)
        p_author = post.__dict__.get("author_id")
        return p_author == user.id

    async def update_post(self, db: DBManager, post: PostSchemaAdd, **ids):
        p_dict = post.model_dump()
        p_id = await db.posts.update_one(p_dict, **ids)
        await db.commit()
        return p_id

    async def delete_post(self, db: DBManager, **ids):
        p_id = await db.posts.delete_one(**ids)
        await db.commit()
        return p_id
