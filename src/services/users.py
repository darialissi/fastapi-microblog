from sqlalchemy.ext.asyncio import AsyncSession

from schemas.users import UserSchema, UserSchemaAdd, UserSchemaUpdate
from utils.password import hash_password
from utils.repository import AbstractRepository


class UsersService:
    def __init__(self, users_repo: AbstractRepository):
        self.users_repo: AbstractRepository = users_repo()

    async def add_user(self, session: AsyncSession, user: UserSchemaAdd):
        u_dict = user.model_dump()
        password = u_dict.pop("password")
        u_dict.update({"hashed_password": hash_password(password).decode("utf-8")})
        u_id = await self.users_repo.add_one(session, u_dict)
        await session.commit()
        return u_id

    async def get_user(self, session: AsyncSession, **filters) -> UserSchema:
        user = await self.users_repo.get_one(session, **filters)
        return user

    async def get_users(self, session, **filters) -> list[UserSchema]:
        users = await self.users_repo.get_all(session, **filters)
        return users

    async def update_user(self, session: AsyncSession, user: UserSchemaUpdate, **ids):
        u_dict = user.model_dump()
        password = u_dict.pop("password")
        u_dict.update({"hashed_password": hash_password(password).decode("utf-8")})
        u_id = await self.users_repo.update_one(session, u_dict, **ids)
        await session.commit()
        return u_id

    async def delete_user(self, session: AsyncSession, **ids):
        u_id = await self.users_repo.delete_one(session, **ids)
        await session.commit()
        return u_id
