from abc import ABC, abstractmethod
from pydantic import BaseModel

from sqlalchemy import select, insert, update, delete

from db.db import async_session


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one():
        raise NotImplementedError
    
    @abstractmethod
    async def get_one():
        raise NotImplementedError
    
    @abstractmethod
    async def get_all():
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    async def add_one(self, data: BaseModel, **ids: int):
        async with async_session() as session:
            add_data = data.model_dump()
            stmt = insert(self.model).values(**add_data, **ids).returning(self.model.id)

            result = await session.execute(stmt)
            await session.commit()
        return result.scalar_one()
    

    async def get_one(self, **filters):
        async with async_session() as session:
            stmt = select(self.model)
            while filters:
                key, val = filters.popitem()
                stmt = stmt.filter(getattr(self.model, key) == val)

            result = await session.execute(stmt)
            return result.scalar_one_or_none()
    

    async def get_all(self, **filters):
        async with async_session() as session:
            stmt = select(self.model)
            while filters:
                key, val = filters.popitem()
                stmt = stmt.filter(getattr(self.model, key) == val)

            result = await session.execute(stmt)
            return result.scalars().all()


    async def update_one(self, data: BaseModel, **ids: int):
        async with async_session() as session:
            update_data = data.model_dump()
            stmt = update(self.model)
            while ids:
                key, val = ids.popitem()
                stmt = stmt.filter(getattr(self.model, key) == val)
            stmt = stmt.values(**update_data).returning(self.model.id)

            result = await session.execute(stmt)
            await session.commit()
        return result.scalar_one()


    async def delete_one(self, **ids: int):
        async with async_session() as session:
            stmt = delete(self.model).returning(self.model.id)
            while ids:
                key, val = ids.popitem()
                stmt = stmt.filter(getattr(self.model, key) == val)

            result = await session.execute(stmt)
            await session.commit()
        return result.scalar_one()