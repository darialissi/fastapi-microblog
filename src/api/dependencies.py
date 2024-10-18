from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import async_session
from utils.unitofwork import DBManager


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with DBManager(async_session) as db:
        yield db


UOW_db = Annotated[DBManager, Depends(get_db)]
