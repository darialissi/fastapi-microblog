from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_cache.decorator import cache

from services.users import UsersService

from .dependencies import UOW_db

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("", summary="Получение всех пользователей")
@cache(expire=30)
async def get_users(
    db: UOW_db,
    service: UsersService = Depends(),
):
    resp = await service.get_users(db)
    if not resp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователи не найдены",
        )
    for user in resp:
        user.__dict__.pop("hashed_password")
    return {"response": resp}


@router.get("/{id_}", summary="Получение пользователя")
@cache(expire=30)
async def get_user(
    id_: int,
    db: UOW_db,
    service: UsersService = Depends(),
):
    resp = await service.get_user(db, id=id_)
    if not resp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Пользователь {id_=} не найден",
        )
    resp.__dict__.pop("hashed_password")
    return {"response": resp}
