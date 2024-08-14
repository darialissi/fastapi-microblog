from schemas.comments import CommentSchemaAdd, CommentSchema, CommentSchemaUpdate
from utils.unitofwork import IUnitOfWork


class CommentsService:

    async def add_comment(self, uow: IUnitOfWork, comment: CommentSchemaAdd, **ids):
        async with uow:
            c_id = await uow.comments.add_one(comment, **ids)
            await uow.commit()
        return c_id

    async def get_comment(self, uow: IUnitOfWork, **filters) -> CommentSchema:
        async with uow:
            comment = await uow.comments.get_one(**filters)
            await uow.commit()
        return comment

    async def get_comments(self, uow: IUnitOfWork, **filters) -> list[CommentSchema]:
        async with uow:
            comments = await uow.comments.get_all(**filters)
            await uow.commit()
        return comments

    async def update_comment(self, uow: IUnitOfWork, data: CommentSchemaUpdate, **ids):
        async with uow:
            c_id = await uow.comments.update_one(data, **ids)
            await uow.commit()
        return c_id

    async def delete_comment(self, uow: IUnitOfWork, **ids):
        async with uow:
            c_id = await uow.comments.delete_one(**ids)
            await uow.commit()
        return c_id