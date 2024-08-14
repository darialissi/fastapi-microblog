from fastapi import APIRouter, HTTPException
from fastapi_cache.decorator import cache

from schemas.users import UserSchemaAdd, UserSchemaUpdate
from services.users import UsersService
from api.dependencies import UOWDep

from sqlalchemy import exc


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("")
async def add_user(
    user: UserSchemaAdd,
    uow: UOWDep,
):
    existed = await UsersService().get_user(uow, username=user.model_dump()["username"])
    if existed:
        raise HTTPException(status_code=400, detail=f"Пользователь с указанным username уже существует")
    resp = await UsersService().add_user(uow, user)
    return {"response": {"id": resp}}


@router.get("")
@cache(expire=30)
async def get_users(
    uow: UOWDep,
):
    resp = await UsersService().get_users(uow)
    if not resp:
        raise HTTPException(status_code=404, detail="Пользователи не найдены")
    return {"response": resp}


@router.get("/{id_}")
@cache(expire=30)
async def get_user(
    id_: int,
    uow: UOWDep,
):
    resp = await UsersService().get_user(uow, id=id_)
    if not resp:
        raise HTTPException(status_code=404, detail=f"Пользователь {id_=} не найден")
    return {"response": resp}


@router.patch("/{id_}")
async def update_user(
    id_: int,
    data: UserSchemaUpdate,
    uow: UOWDep,
):
    try:
        resp = await UsersService().update_user(uow, data, id=id_)
    except exc.NoResultFound:
        raise HTTPException(status_code=400, detail=f"Пользователь {id_=} не существует")
    return {"response": {"id": resp}}


@router.delete("/{id_}")
async def delete_user(
    id_: int,
    uow: UOWDep,
):
    try:
        resp = await UsersService().delete_user(uow, id=id_)
    except exc.NoResultFound:
        raise HTTPException(status_code=400, detail=f"Пользователь {id_=} не существует")
    return {"response": {"id": resp}}
