from fastapi import APIRouter, HTTPException
from fastapi_cache.decorator import cache

from schemas.comments import CommentSchemaAdd, CommentSchemaUpdate
from services.comments import CommentsService
from api.dependencies import UOWDep

from sqlalchemy import exc


router = APIRouter(
    prefix="/{post_id}/comments",
)


@router.post("")
async def add_comment(
    post_id: int,
    comment: CommentSchemaAdd,
    uow: UOWDep,
):
    try:
        resp = await CommentsService().add_comment(uow, comment, post_id=post_id)
    except exc.IntegrityError as e:
        raise HTTPException(status_code=400, detail=f"{e.orig.args[0]}")
    return {"response": {"id": resp}}


@router.get("")
@cache(expire=30)
async def get_comments(
    post_id: int,
    uow: UOWDep,
):
    resp = await CommentsService().get_comments(uow, post_id=post_id)
    if not resp:
        raise HTTPException(status_code=404, detail=f"Комментарии {post_id=} не найдены")
    return {"response": resp}


@router.get("/{id_}")
async def get_comment(
    post_id: int,
    id_: int,
    uow: UOWDep,
):
    resp = await CommentsService().get_comment(uow, post_id=post_id, id=id_)
    if not resp:
        raise HTTPException(status_code=404, detail=f"Комментарий {id_=}, {post_id=} не найден")
    return {"response": resp}


@router.patch("/{id_}")
async def update_comment(
    post_id: int,
    id_: int,
    data: CommentSchemaUpdate,
    uow: UOWDep,
):
    try:
        resp = await CommentsService().update_comment(uow, data, post_id=post_id, id=id_)
    except exc.NoResultFound:
        raise HTTPException(status_code=400, detail=f"Комментарий {id_=}, {post_id=} не существует")
    return {"response": {"id": resp}}


@router.delete("/{id_}")
async def delete_post(
    post_id: int,
    id_: int,
    uow: UOWDep,
):
    try:
        resp = await CommentsService().delete_comment(uow, post_id=post_id, id=id_)
    except exc.NoResultFound:
        raise HTTPException(status_code=400, detail=f"Комментарий {id_=}, {post_id=} не существует")
    return {"response": {"id": resp}}