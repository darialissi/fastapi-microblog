from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_async_session
from repositories.comments import CommentsRepository
from repositories.posts import PostsRepository
from repositories.users import UsersRepository
from services.comments import CommentsService
from services.posts import PostsService
from services.users import UsersService

session = Annotated[AsyncSession, Depends(get_async_session)]


def posts_service():
    return PostsService(PostsRepository)


def comments_service():
    return CommentsService(CommentsRepository)


def users_service():
    return UsersService(UsersRepository)
