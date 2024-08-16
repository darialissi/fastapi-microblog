from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from repositories.posts import PostsRepository
from repositories.users import UsersRepository
from repositories.comments import CommentsRepository

from services.posts import PostsService
from services.users import UsersService
from services.comments import CommentsService

from db.db import get_async_session


session = Annotated[AsyncSession, Depends(get_async_session)]

def posts_service():
    return PostsService(PostsRepository)

def comments_service():
    return CommentsService(CommentsRepository)

def users_service():
    return UsersService(UsersRepository)