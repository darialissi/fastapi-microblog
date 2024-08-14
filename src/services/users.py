from schemas.users import UserSchemaAdd, UserSchema, UserSchemaUpdate
from utils.unitofwork import IUnitOfWork


class UsersService:

    async def add_user(self, uow: IUnitOfWork, user: UserSchemaAdd):
        async with uow:
            u_id = await uow.users.add_one(user)
            await uow.commit()
        return u_id

    async def get_user(self, uow: IUnitOfWork, **filters) -> UserSchema:
        async with uow:
            user = await uow.users.get_one(**filters)
            await uow.commit()
        return user

    async def get_users(self, uow: IUnitOfWork, **filters) -> list[UserSchema]:
        async with uow:
            users = await uow.users.get_all(**filters)
            await uow.commit()
        return users

    async def update_user(self, uow: IUnitOfWork, data: UserSchemaUpdate, **ids):
        async with uow:
            u_id = await uow.users.update_one(data, **ids)
            await uow.commit()
        return u_id

    async def delete_user(self, uow: IUnitOfWork, **ids):
        async with uow:
            u_id = await uow.users.delete_one(**ids)
            await uow.commit()
        return u_id