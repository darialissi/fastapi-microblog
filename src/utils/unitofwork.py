from sqlalchemy.ext.asyncio import AsyncSession

from repositories.comments import CommentsRepository
from repositories.posts import PostsRepository
from repositories.users import UsersRepository


class DBManager:

    def __init__(self, session: AsyncSession):
        self.session_factory = session

    async def __aenter__(self):
        self.session = self.session_factory()

        self.users = UsersRepository(self.session)
        self.posts = PostsRepository(self.session)
        self.comments = CommentsRepository(self.session)

        return self

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
