from schemas.users import UserSchema, UserSchemaAdd, UserSchemaID
from utils.password import Password
from utils.unitofwork import DBManager


class UsersService:

    async def add_user(self, db: DBManager, user: UserSchemaAdd) -> UserSchemaID:
        u_dict = user.model_dump()
        password = u_dict.pop("password")
        u_dict.update({"hashed_password": Password.hash_password(password)})
        u_id = await db.users.add_one(u_dict)
        await db.commit()
        return UserSchemaID.model_validate({"id": u_id})

    async def get_user(self, db: DBManager, **filters) -> UserSchema:
        if user := await db.users.get_one(**filters):
            return UserSchema.model_validate(user)

    async def get_users(self, db: DBManager, **filters) -> list[UserSchema]:
        if users := await db.users.get_all(**filters):
            return [UserSchema.model_validate(user) for user in users]

    async def update_user(self, db: DBManager, user: UserSchemaAdd, **ids) -> UserSchemaID:
        u_dict = user.model_dump()
        password = u_dict.pop("password")
        u_dict.update({"hashed_password": Password.hash_password(password)})
        u_id = await db.users.update_one(u_dict, **ids)
        await db.commit()
        return UserSchemaID.model_validate({"id": u_id})

    async def delete_user(self, db: DBManager, **ids) -> UserSchemaID:
        u_id = await db.users.delete_one(**ids)
        await db.commit()
        return UserSchemaID.model_validate({"id": u_id})
