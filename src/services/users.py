from schemas.users import UserSchemaAdd, UserSchema, UserSchemaUpdate
from utils.repository import AbstractRepository


class UsersService:
    def __init__(self, users_repo: AbstractRepository):
        self.users_repo: AbstractRepository = users_repo()

    async def add_user(self, user: UserSchemaAdd) -> dict:
        user_id = await self.users_repo.add_one(user)
        return user_id

    async def get_user(self, **filters) -> list[UserSchema]:
        user = await self.users_repo.get_one(**filters)
        return user

    async def get_users(self, **filters) -> list[UserSchema]:
        users = await self.users_repo.get_all(**filters)
        return users

    async def update_user(self, data: UserSchemaUpdate, **ids) -> dict:
        response = await self.users_repo.update_one(data, **ids)
        return response

    async def delete_user(self, **ids) -> dict:
        response = await self.users_repo.delete_one(**ids)
        return response