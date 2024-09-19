from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_cache.decorator import cache
from sqlalchemy import exc

from api.dependencies import comments_service, session
from schemas.comments import CommentSchemaAdd, CommentSchemaUpdate
from services.comments import CommentsService

from .auth.router import get_current_user

router = APIRouter(
    prefix="/{post_id}/comments",
)

Service = Annotated[CommentsService, Depends(comments_service)]


@router.post("", status_code=status.HTTP_201_CREATED, summary="Добавление нового комментария")
async def add_comment(
    post_id: int,
    comment: CommentSchemaAdd,
    comments_service: Service,
    session: session,
    user: str = Depends(get_current_user),
):
    try:
        resp = await comments_service.add_comment(session, user, comment, post_id=post_id)
    except exc.IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{e.orig.args[0]}",
        )
    return {"response": {"id": resp}}


@router.get("", summary="Получение всех комментариев к посту")
@cache(expire=30)
async def get_comments(
    post_id: int,
    comments_service: Service,
    session: session,
):
    resp = await comments_service.get_comments(session, post_id=post_id)
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
    comments_service: Service,
    session: session,
):
    resp = await comments_service.get_comment(session, post_id=post_id, id=id_)
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
    data: CommentSchemaUpdate,
    comments_service: Service,
    session: session,
    user: str = Depends(get_current_user),
):
    try:
        resp = await comments_service.update_comment(session, data, post_id=post_id, id=id_)
    except exc.NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Комментарий {id_=}, {post_id=} не существует",
        )
    return {"response": {"id": resp}}


@router.delete("/{id_}", summary="Удаление комментария")
async def delete_post(
    post_id: int,
    id_: int,
    comments_service: Service,
    session: session,
    user: str = Depends(get_current_user),
):
    try:
        resp = await comments_service.delete_comment(session, post_id=post_id, id=id_)
    except exc.NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Комментарий {id_=}, {post_id=} не существует",
        )
    return {"response": {"id": resp}}
