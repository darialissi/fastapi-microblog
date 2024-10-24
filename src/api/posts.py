from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_cache.decorator import cache
from sqlalchemy import exc

from api.dependencies import UOW_db
from schemas.posts import PostSchemaAdd
from schemas.users import UserSchemaAuth
from services.posts import PostsService

from .auth.router import get_current_user

router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
)


@router.post("", status_code=status.HTTP_201_CREATED, summary="Добавление нового поста")
async def add_post(
    post: PostSchemaAdd,
    db: UOW_db,
    service: PostsService = Depends(),
    user: UserSchemaAuth = Depends(get_current_user),
):
    try:
        resp = await service.add_post(db, user, post)
    except exc.IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{e.orig.args[0]}",
        )
    return {"response": resp}


@router.get("", summary="Получение всех постов пользователя")
@cache(expire=30)
async def get_posts(
    db: UOW_db,
    service: PostsService = Depends(),
):
    resp = await service.get_posts(db)
    if not resp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Посты не найдены",
        )
    return {"response": resp}


@router.get("/{id_}", summary="Получение поста")
@cache(expire=30)
async def get_post(
    id_: int,
    db: UOW_db,
    service: PostsService = Depends(),
):
    resp = await service.get_post(db, id=id_)
    if not resp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Пост {id_=} не найден",
        )
    return {"response": resp}


@router.patch("/{id_}", summary="Обновление поста")
async def update_post(
    id_: int,
    data: PostSchemaAdd,
    db: UOW_db,
    service: PostsService = Depends(),
    user: UserSchemaAuth = Depends(get_current_user),
):
    if not await service.validate_author_post(db, user, post_id=id_):
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail=f"Пользователь {user.username} не является автором поста {id_=}",
        )
    try:
        resp = await service.update_post(db, data, id=id_)
    except exc.NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Пост {id_=} не существует",
        )
    return {"response": resp}


@router.delete("/{id_}", summary="Удаление поста")
async def delete_post(
    id_: int,
    db: UOW_db,
    service: PostsService = Depends(),
    user: UserSchemaAuth = Depends(get_current_user),
):
    if not await service.validate_author_post(db, user, post_id=id_):
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail=f"Пользователь {user.username} не является автором поста {id_=}",
        )
    try:
        resp = await service.delete_post(db, id=id_)
    except exc.NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Пост {id_=} не существует",
        )
    return {"response": resp}
