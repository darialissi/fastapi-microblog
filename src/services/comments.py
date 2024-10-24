from schemas.comments import CommentSchema, CommentSchemaAdd, CommentSchemaID
from schemas.users import UserSchemaAuth
from utils.unitofwork import DBManager


class CommentsService:

    async def add_comment(
        self, db: DBManager, user: UserSchemaAuth, comment: CommentSchemaAdd, **ids
    ) -> CommentSchemaID:
        c_dict = comment.model_dump()
        c_dict.update({"author_id": user.id})
        c_id = await db.comments.add_one(c_dict, **ids)
        await db.commit()
        return CommentSchemaID.model_validate({"id": c_id})

    async def get_comment(self, db: DBManager, **filters) -> CommentSchema:
        if comment := await db.comments.get_one(**filters):
            return CommentSchema.model_validate(comment)

    async def get_comments(self, db: DBManager, **filters) -> list[CommentSchema]:
        if comments := await db.comments.get_all(**filters):
            return [CommentSchema.model_validate(comment) for comment in comments]

    async def validate_author_comment(self, db: DBManager, user: UserSchemaAuth, post_id: int, comment_id: int) -> bool:
        comment = await db.comments.get_one(post_id=post_id, id=comment_id)
        c_author = comment.__dict__.get("author_id")
        return c_author == user.id

    async def update_comment(self, db: DBManager, comment: CommentSchemaAdd, **ids) -> CommentSchemaID:
        c_dict = comment.model_dump()
        c_id = await db.comments.update_one(c_dict, **ids)
        await db.commit()
        return CommentSchemaID.model_validate({"id": c_id})

    async def delete_comment(self, db: DBManager, **ids) -> CommentSchemaID:
        c_id = await db.comments.delete_one(**ids)
        await db.commit()
        return CommentSchemaID.model_validate({"id": c_id})
