from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from api.dependencies import posts_service
from schemas.posts import PostSchemaAdd, PostSchemaUpdate
from services.posts import PostsService


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
    resp = await posts_service.add_post(post)
    return resp


@router.get("")
@cache(expire=30)
async def get_posts(
    posts_service: service,
):
    resp = await posts_service.get_posts()
    return resp


@router.get("/{id_}")
@cache(expire=30)
async def get_post(
    id_: int,
    posts_service: service,
):
    resp = await posts_service.get_post(id=id_)
    return resp


@router.patch("/{id_}")
async def update_post(
    id_: int,
    data: PostSchemaUpdate,
    posts_service: service,
):
    resp = await posts_service.update_post(data, id=id_)
    return resp


@router.delete("/{id_}")
async def delete_post(
    id_: int,
    posts_service: service,
):
    resp = await posts_service.delete_post(id=id_)
    return resp



