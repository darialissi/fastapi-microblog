from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache

from api.dependencies import comments_service
from schemas.comments import CommentSchemaAdd, CommentSchemaUpdate
from services.comments import CommentsService

from sqlalchemy import exc

router = APIRouter(
    prefix="/{post_id}/comments",
)

service = Annotated[CommentsService, Depends(comments_service)]

@router.post("")
async def add_comment(
    post_id: int,
    comment: CommentSchemaAdd,
    comments_service: service,
):
    try:
        resp = await comments_service.add_comment(comment, post_id=post_id)
    except exc.IntegrityError as e:
        raise HTTPException(status_code=400, detail=f"{e.orig.args[0]}")
    return {"response": {"id": resp}}


@router.get("")
@cache(expire=30)
async def get_comments(
    post_id: int,
    comments_service: service,
):
    resp = await comments_service.get_comments(post_id=post_id)
    if not resp:
        raise HTTPException(status_code=404, detail=f"Комментарии {post_id=} не найдены")
    return {"response": resp}


@router.get("/{id_}")
async def get_comment(
    post_id: int,
    id_: int,
    comments_service: service,
):
    resp = await comments_service.get_comment(post_id=post_id, id=id_)
    if not resp:
        raise HTTPException(status_code=404, detail=f"Комментарий {id_=}, {post_id=} не найден")
    return {"response": resp}


@router.patch("/{id_}")
async def update_comment(
    post_id: int,
    id_: int,
    data: CommentSchemaUpdate,
    comments_service: service,
):
    try:
        resp = await comments_service.update_comment(data, post_id=post_id, id=id_)
    except exc.NoResultFound:
        raise HTTPException(status_code=400, detail=f"Комментарий {id_=}, {post_id=} не существует")
    return {"response": {"id": resp}}


@router.delete("/{id_}")
async def delete_post(
    post_id: int,
    id_: int,
    comments_service: service,
):
    try:
        resp = await comments_service.delete_comment(post_id=post_id, id=id_)
    except exc.NoResultFound:
        raise HTTPException(status_code=400, detail=f"Комментарий {id_=}, {post_id=} не существует")
    return {"response": {"id": resp}}