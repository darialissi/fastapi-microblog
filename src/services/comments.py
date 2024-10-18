from models.users import User
from schemas.comments import CommentSchema, CommentSchemaAdd
from schemas.users import UserSchema
from utils.unitofwork import DBManager


class CommentsService:

    async def add_comment(self, db: DBManager, user: User, comment: CommentSchemaAdd, **ids):
        c_dict = comment.model_dump()
        c_dict.update({"author_id": user.id})
        c_id = await db.comments.add_one(c_dict, **ids)
        await db.commit()
        return c_id

    async def get_comment(self, db: DBManager, **filters) -> CommentSchema:
        comment = await db.comments.get_one(**filters)
        return comment

    async def get_comments(self, db: DBManager, **filters) -> list[CommentSchema]:
        comments = await db.comments.get_all(**filters)
        return comments

    async def validate_author_comment(self, db: DBManager, user: UserSchema, post_id: int, comment_id: int):
        comment = await db.comments.get_one(post_id=post_id, id=comment_id)
        c_author = comment.__dict__.get("author_id")
        return c_author == user.id

    async def update_comment(self, db: DBManager, comment: CommentSchemaAdd, **ids):
        c_dict = comment.model_dump()
        c_id = await db.comments.update_one(c_dict, **ids)
        await db.commit()
        return c_id

    async def delete_comment(self, db: DBManager, **ids):
        c_id = await db.comments.delete_one(**ids)
        await db.commit()
        return c_id
