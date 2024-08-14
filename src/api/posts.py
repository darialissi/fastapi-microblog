from fastapi import APIRouter, HTTPException
from fastapi_cache.decorator import cache

from schemas.posts import PostSchemaAdd, PostSchemaUpdate
from services.posts import PostsService
from api.dependencies import UOWDep

from sqlalchemy import exc


router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
)


@router.post("")
async def add_post(
    post: PostSchemaAdd,
    uow: UOWDep,
):
    try:
        resp = await PostsService().add_post(uow, post)
    except exc.IntegrityError as e:
        raise HTTPException(status_code=400, detail=f"{e.orig.args[0]}")
    return {"response": {"id": resp}}


@router.get("")
@cache(expire=30)
async def get_posts(
    uow: UOWDep,
):
    resp = await PostsService().get_posts(uow)
    if not resp:
        raise HTTPException(status_code=404, detail="Посты не найдены")
    return {"response": resp}


@router.get("/{id_}")
@cache(expire=30)
async def get_post(
    id_: int,
    uow: UOWDep,
):
    resp = await PostsService().get_post(uow, id=id_)
    if not resp:
        raise HTTPException(status_code=404, detail=f"Пост {id_=} не найден")
    return {"response": resp}


@router.patch("/{id_}")
async def update_post(
    id_: int,
    data: PostSchemaUpdate,
    uow: UOWDep,
):
    try:
        resp = await PostsService().update_post(uow, data, id=id_)
    except exc.NoResultFound:
        raise HTTPException(status_code=400, detail=f"Пост {id_=} не существует")
    return {"response": {"id": resp}}


@router.delete("/{id_}")
async def delete_post(
    id_: int,
    uow: UOWDep,
):
    try:
        resp = await PostsService().delete_post(uow, id=id_)
    except exc.NoResultFound:
        raise HTTPException(status_code=400, detail=f"Пост {id_=} не существует")
    return {"response": {"id": resp}}



