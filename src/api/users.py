from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_cache.decorator import cache

from api.dependencies import users_service, session
from services.users import UsersService


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

service = Annotated[UsersService, Depends(users_service)]


@router.get("")
@cache(expire=30)
async def get_users(
    users_service: service,
    session: session,
):
    resp = await users_service.get_users(session)
    if not resp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователи не найдены",
        )
    for user in resp:
        user.__dict__.pop("hashed_password")
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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Пользователь {id_=} не найден",
        )
    resp.__dict__.pop("hashed_password")
    return {"response": resp}
