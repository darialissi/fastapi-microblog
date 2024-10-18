from schemas.users import UserSchema, UserSchemaAdd
from utils.password import hash_password
from utils.unitofwork import DBManager


class UsersService:

    async def add_user(self, db: DBManager, user: UserSchemaAdd):
        u_dict = user.model_dump()
        password = u_dict.pop("password")
        u_dict.update({"hashed_password": hash_password(password).decode("utf-8")})
        u_id = await db.users.add_one(u_dict)
        await db.commit()
        return u_id

    async def get_user(self, db: DBManager, **filters) -> UserSchema:
        user = await db.users.get_one(**filters)
        return user

    async def get_users(self, db: DBManager, **filters) -> list[UserSchema]:
        users = await db.users.get_all(**filters)
        return users

    async def update_user(self, db: DBManager, user: UserSchemaAdd, **ids) -> int:
        u_dict = user.model_dump()
        password = u_dict.pop("password")
        u_dict.update({"hashed_password": hash_password(password).decode("utf-8")})
        u_id = await db.users.update_one(u_dict, **ids)
        await db.commit()
        return u_id

    async def delete_user(self, db: DBManager, **ids):
        u_id = await db.users.delete_one(**ids)
        await db.commit()
        return u_id
