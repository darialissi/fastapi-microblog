from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import ExpiredSignatureError

from api.dependencies import Redis_db, UOW_db
from schemas.users import UserSchemaAdd, UserSchemaAuth
from services.users import UsersService
from utils.password import Password

from .redis import RedisStorage
from .schemas import TokenSchema
from .token import Token

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


@router.post("/register", status_code=status.HTTP_201_CREATED, summary="Регистрация нового пользователя")
async def add_user(
    user: UserSchemaAdd,
    db: UOW_db,
    service: UsersService = Depends(),
):
    existed = await service.get_user(db, username=user.username)
    if existed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с указанным username уже существует",
        )
    resp = await service.add_user(db, user)
    return {"response": resp}


@router.post("/token", summary="Получение access и refresh токена")
async def auth_user(
    db: UOW_db,
    redis: Redis_db,
    service: UsersService = Depends(),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    if not (user := await service.get_user(db, username=form_data.username)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not Password.validate_password(password=form_data.password, hashed_password=user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token, refresh_token = Token.generate_tokens(user.id, user.username)

    await RedisStorage.add_token(redis_client=redis, key=f"user:{user.id}", value=refresh_token)

    return TokenSchema(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", summary="Обновление access и refresh токена")
async def refresh_token(redis: Redis_db, grant_type: str = Form("refresh_token"), refresh_token: str = Form()):

    try:
        payload = Token.decode_jwt(refresh_token)

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token has been expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_sub = payload.get("sub")

    valid_token = await RedisStorage.get_token(redis_client=redis, key=user_sub)

    if refresh_token != valid_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token is not valid",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = int(user_sub.split(":")[-1])
    username = payload.get("username")

    access_token, refresh_token = Token.generate_tokens(user_id, username)

    await RedisStorage.add_token(redis_client=redis, key=user_sub, value=refresh_token)

    return TokenSchema(access_token=access_token, refresh_token=refresh_token)


async def get_current_user(
    db: UOW_db,
    service: UsersService = Depends(),
    token: str = Depends(oauth2_scheme),
) -> UserSchemaAuth:

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = Token.decode_jwt(token)

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = int(payload.get("sub").split(":")[-1])

    if not (user := await service.get_user(db, id=user_id)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist",
            headers={"WWW-Authenticate": "Bearer"},
        )

    resp = user.model_dump()
    resp.pop("hashed_password")
    logged_in_at = datetime.fromtimestamp(payload.get("iat"), tz=timezone.utc)
    resp.update({"logged_in_at": logged_in_at})

    return UserSchemaAuth(**resp)


@router.get("/account", summary="Получение авторизованного аккаунта")
async def get_auth_user(
    user: UserSchemaAuth = Depends(get_current_user),
):
    return {"response": user}


@router.patch("/account", summary="Обновление авторизованного аккаунта")
async def update_auth_user(
    data: UserSchemaAdd,
    db: UOW_db,
    service: UsersService = Depends(),
    user: UserSchemaAuth = Depends(get_current_user),
):
    existed = await service.get_user(db, username=data.username)

    if existed and existed.username != data.username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с указанным username уже существует",
        )

    resp = await service.update_user(db, data, id=user.id)
    return {"response": resp}


@router.delete("/account", summary="Удаление авторизованного аккаунта")
async def delete_auth_user(
    db: UOW_db,
    redis: Redis_db,
    service: UsersService = Depends(),
    user: UserSchemaAuth = Depends(get_current_user),
):

    resp = await service.delete_user(db, id=user.id)

    await RedisStorage.revoke_token(redis_client=redis, key=f"user:{user.id}")

    return {"response": resp}
