from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import ExpiredSignatureError

from api.dependencies import session
from api.users import Service
from models.users import User
from schemas.users import UserSchemaAdd, UserSchemaUpdate
from utils.password import validate_password

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
    users_service: Service,
    session: session,
):
    existed = await users_service.get_user(session, username=user.model_dump()["username"])
    if existed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с указанным username уже существует",
        )
    resp = await users_service.add_user(session, user)
    return {"response": {"id": resp}}


@router.post("/token", summary="Получение access и refresh токена")
async def auth_user(
    session: session,
    user_service: Service,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    if not (user := await user_service.get_user(session=session, username=form_data.username)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not validate_password(password=form_data.password, hashed_password=user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token, refresh_token = await Token.generate_tokens(user.id, user.username)

    return TokenSchema(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh-token", summary="Обновление access и refresh токена")
async def refresh_token(grant_type: str = Form("refresh_token"), refresh_token: str = Form()):
    """
    Issue new tokens by refresh token
    """
    try:
        payload = Token.decode_jwt(refresh_token)

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token has been expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_sub = payload.get("sub")
    user_id = int(user_sub.split(":")[-1])
    username = payload.get("username")

    await RedisStorage.revoke_token(user_sub)
    access_token, refresh_token = await Token.generate_tokens(user_id, username)

    return TokenSchema(access_token=access_token, refresh_token=refresh_token)


async def get_current_user(
    users_service: Service,
    session: session,
    token: str = Depends(oauth2_scheme),
) -> User:
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
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token has been expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = int(payload.get("sub").split(":")[-1])

    resp = await users_service.get_user(session, id=user_id)
    resp.__dict__.pop("hashed_password")

    logged_in_at = datetime.fromtimestamp(payload.get("iat"), tz=timezone.utc)
    resp.__dict__.update({"logged_in_at": logged_in_at})
    return resp


@router.get("/account", summary="Получение авторизованного аккаунта")
async def get_auth_user(
    user: str = Depends(get_current_user),
):
    return {"response": user}


@router.patch("/account", summary="Обновление авторизованного аккаунта")
async def update_auth_user(
    data: UserSchemaUpdate,
    users_service: Service,
    session: session,
    user: str = Depends(get_current_user),
):
    existed = await users_service.get_user(session, username=data.username)

    if existed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с указанным username уже существует",
        )

    resp = await users_service.update_user(session, data, id=user.id)
    return {"response": {"id": resp}}


@router.delete("/account", summary="Удаление авторизованного аккаунта")
async def delete_auth_user(
    users_service: Service,
    session: session,
    user: str = Depends(get_current_user),
):

    resp = await users_service.delete_user(session, id=user.id)
    return {"response": {"id": resp}}
