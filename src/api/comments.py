from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_cache.decorator import cache
from sqlalchemy import exc

from api.dependencies import UOW_db
from schemas.comments import CommentSchemaAdd
from schemas.users import UserSchemaAuth
from services.comments import CommentsService

from .auth.router import get_current_user

router = APIRouter(
    prefix="/{post_id}/comments",
)


@router.post("", status_code=status.HTTP_201_CREATED, summary="Добавление нового комментария")
async def add_comment(
    post_id: int,
    comment: CommentSchemaAdd,
    db: UOW_db,
    service: CommentsService = Depends(),
    user: UserSchemaAuth = Depends(get_current_user),
):
    try:
        resp = await service.add_comment(db, user, comment, post_id=post_id)
    except exc.IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{e.orig.args[0]}",
        )
    return {"response": resp}


@router.get("", summary="Получение всех комментариев к посту")
@cache(expire=30)
async def get_comments(
    post_id: int,
    db: UOW_db,
    service: CommentsService = Depends(),
):
    resp = await service.get_comments(db, post_id=post_id)
    if not resp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Комментарии {post_id=} не найдены",
        )
    return {"response": resp}


@router.get("/{id_}", summary="Получение комментария")
async def get_comment(
    post_id: int,
    id_: int,
    db: UOW_db,
    service: CommentsService = Depends(),
):
    resp = await service.get_comment(db, post_id=post_id, id=id_)
    if not resp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Комментарий {id_=}, {post_id=} не найден",
        )
    return {"response": resp}


@router.patch("/{id_}", summary="Обновление комментария")
async def update_comment(
    post_id: int,
    id_: int,
    data: CommentSchemaAdd,
    db: UOW_db,
    service: CommentsService = Depends(),
    user: UserSchemaAuth = Depends(get_current_user),
):

    if not (comment := await service.get_comment(db, post_id=post_id, id=id_)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Комментарий {id_=}, {post_id=} не существует",
        )

    if not service.is_author_comment(user.id, comment.author_id):
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail=f"Пользователь {user.username} не является автором комментария {id_=}",
        )

    resp = await service.update_comment(db, data, post_id=post_id, id=id_)

    return {"response": resp}


@router.delete("/{id_}", summary="Удаление комментария")
async def delete_post(
    post_id: int,
    id_: int,
    db: UOW_db,
    service: CommentsService = Depends(),
    user: UserSchemaAuth = Depends(get_current_user),
):

    if not (comment := await service.get_comment(db, post_id=post_id, id=id_)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Комментарий {id_=}, {post_id=} не существует",
        )

    if not service.is_author_comment(user.id, comment.author_id):
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail=f"Пользователь {user.username} не является автором комментария {id_=}",
        )

    resp = await service.delete_comment(db, post_id=post_id, id=id_)

    return {"response": resp}
