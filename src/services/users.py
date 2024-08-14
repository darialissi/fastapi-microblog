from schemas.users import UserSchemaAdd, UserSchema, UserSchemaUpdate
from utils.repository import AbstractRepository
from hashlib import sha512


class UsersService:
    def __init__(self, users_repo: AbstractRepository):
        self.users_repo: AbstractRepository = users_repo()

    async def add_user(self, user: UserSchemaAdd):
        user.password = sha512(user.model_dump()["password"].encode()).hexdigest()
        u_id = await self.users_repo.add_one(user)
        return u_id

    async def get_user(self, **filters) -> UserSchema:
        user = await self.users_repo.get_one(**filters)
        return user

    async def get_users(self, **filters) -> list[UserSchema]:
        users = await self.users_repo.get_all(**filters)
        return users

    async def update_user(self, data: UserSchemaUpdate, **ids):
        data.password = sha512(data.model_dump()["password"].encode()).hexdigest()
        u_id = await self.users_repo.update_one(data, **ids)
        return u_id

    async def delete_user(self, **ids):
        u_id = await self.users_repo.delete_one(**ids)
        return u_id