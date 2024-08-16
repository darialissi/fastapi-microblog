from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_cache.decorator import cache

from api.dependencies import users_service, session
from schemas.users import UserSchemaAdd, UserSchemaUpdate
from services.users import UsersService

from sqlalchemy import exc

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

service = Annotated[UsersService, Depends(users_service)]

@router.post("", status_code=status.HTTP_201_CREATED)
async def add_user(
    user: UserSchemaAdd,
    users_service: service,
    session: session,
):
    existed = await users_service.get_user(session, username=user.model_dump()["username"])
    if existed:
        raise HTTPException(status_code=400, detail=f"Пользователь с указанным username уже существует")
    resp = await users_service.add_user(session, user)
    return {"response": {"id": resp}}


@router.get("")
@cache(expire=30)
async def get_users(
    users_service: service,
    session: session,
):
    resp = await users_service.get_users(session)
    if not resp:
        raise HTTPException(status_code=404, detail="Пользователи не найдены")
    return {"response": resp}


@router.get("/{id_}")
@cache(expire=30)
async def get_user(
    id_: int,
    users_service: service,
    session: session,
):
    resp = await users_service.get_user(session, id=id_)
    if not resp:
        raise HTTPException(status_code=404, detail=f"Пользователь {id_=} не найден")
    return {"response": resp}


@router.patch("/{id_}")
async def update_user(
    id_: int,
    data: UserSchemaUpdate,
    users_service: service,
    session: session,
):
    try:
        resp = await users_service.update_user(session, data, id=id_)
    except exc.NoResultFound:
        raise HTTPException(status_code=400, detail=f"Пользователь {id_=} не существует")
    return {"response": {"id": resp}}


@router.delete("/{id_}")
async def delete_user(
    id_: int,
    users_service: service,
    session: session,
):
    try:
        resp = await users_service.delete_user(session, id=id_)
    except exc.NoResultFound:
        raise HTTPException(status_code=400, detail=f"Пользователь {id_=} не существует")
    return {"response": {"id": resp}}
