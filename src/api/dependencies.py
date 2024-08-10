from repositories.posts import PostsRepository
from repositories.users import UsersRepository
from repositories.comments import CommentsRepository

from services.posts import PostsService
from services.users import UsersService
from services.comments import CommentsService


def posts_service():
    return PostsService(PostsRepository)


def comments_service():
    return CommentsService(CommentsRepository)


def users_service():
    return UsersService(UsersRepository)