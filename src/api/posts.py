from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache

from api.dependencies import posts_service
from schemas.posts import PostSchemaAdd, PostSchemaUpdate
from services.posts import PostsService

from sqlalchemy import exc


router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
)

service = Annotated[PostsService, Depends(posts_service)]

@router.post("")
async def add_post(
    post: PostSchemaAdd,
    posts_service: service,
):
    try:
        resp = await posts_service.add_post(post)
    except exc.IntegrityError as e:
        raise HTTPException(status_code=400, detail=f"{e.orig.args[0]}")
    return {"response": {"id": resp}}


@router.get("")
@cache(expire=30)
async def get_posts(
    posts_service: service,
):
    resp = await posts_service.get_posts()
    if not resp:
        raise HTTPException(status_code=404, detail="Посты не найдены")
    return {"response": resp}


@router.get("/{id_}")
@cache(expire=30)
async def get_post(
    id_: int,
    posts_service: service,
):
    resp = await posts_service.get_post(id=id_)
    if not resp:
        raise HTTPException(status_code=404, detail=f"Пост {id_=} не найден")
    return {"response": resp}


@router.patch("/{id_}")
async def update_post(
    id_: int,
    data: PostSchemaUpdate,
    posts_service: service,
):
    try:
        resp = await posts_service.update_post(data, id=id_)
    except exc.NoResultFound:
        raise HTTPException(status_code=400, detail=f"Пост {id_=} не существует")
    return {"response": {"id": resp}}


@router.delete("/{id_}")
async def delete_post(
    id_: int,
    posts_service: service,
):
    try:
        resp = await posts_service.delete_post(id=id_)
    except exc.NoResultFound:
        raise HTTPException(status_code=400, detail=f"Пост {id_=} не существует")
    return {"response": {"id": resp}}



