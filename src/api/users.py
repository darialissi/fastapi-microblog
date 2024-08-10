from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from api.dependencies import users_service
from schemas.users import UserSchemaAdd, UserSchemaUpdate
from services.users import UsersService

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

service = Annotated[UsersService, Depends(users_service)]

@router.post("")
async def add_user(
    user: UserSchemaAdd,
    users_service: service,
):
    resp = await users_service.add_user(user)
    return resp


@router.get("")
@cache(expire=30)
async def get_users(
    users_service: service,
):
    resp = await users_service.get_users()
    return resp


@router.get("/{id_}")
@cache(expire=30)
async def get_user(
    id_: int,
    users_service: service,
):
    resp = await users_service.get_user(id=id_)
    return resp


@router.patch("/{id_}")
async def update_user(
    id_: int,
    data: UserSchemaUpdate,
    users_service: service,
):
    resp = await users_service.update_user(data, id=id_)
    return resp


@router.delete("/{id_}")
async def delete_user(
    id_: int,
    users_service: service,
):
    resp = await users_service.delete_user(id=id_)
    return resp
