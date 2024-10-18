from abc import ABC, abstractmethod

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession


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

    @abstractmethod
    async def update_one():
        raise NotImplementedError

    @abstractmethod
    async def delete_one():
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data: dict, **ids: int):
        stmt = insert(self.model).values(**data, **ids).returning(self.model.id)

        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def get_one(self, **filters):
        stmt = select(self.model)
        while filters:
            key, val = filters.popitem()
            stmt = stmt.filter(getattr(self.model, key) == val)

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self, **filters):
        stmt = select(self.model)
        while filters:
            key, val = filters.popitem()
            stmt = stmt.filter(getattr(self.model, key) == val)

        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update_one(self, data: dict, **ids: int):
        stmt = update(self.model)
        while ids:
            key, val = ids.popitem()
            stmt = stmt.filter(getattr(self.model, key) == val)
        stmt = stmt.values(**data).returning(self.model.id)

        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def delete_one(self, **ids: int):
        stmt = delete(self.model).returning(self.model.id)
        while ids:
            key, val = ids.popitem()
            stmt = stmt.filter(getattr(self.model, key) == val)

        result = await self.session.execute(stmt)
        return result.scalar_one()
