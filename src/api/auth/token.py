from datetime import datetime, timedelta, timezone

import jwt
from jwt.exceptions import ExpiredSignatureError

from config import settings
from db.db import redis_client

from .redis import RedisStorage
from .schemas import TokenType

# /certs - в корне приложения
# openssl genrsa -out jwt-private.pem 2048
# openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem

# >>> private_key = b"-----BEGIN PRIVATE KEY-----\nMIGEAgEAMBAGByqGSM49AgEGBS..."\
# >>> public_key = b"-----BEGIN PUBLIC KEY-----\nMHYwEAYHKoZIzj0CAQYFK4EEAC..."


class Token:

    @staticmethod
    def encode_jwt(
        payload: dict,
        expire: timedelta,
        private_key: str = settings.jwt.private_key_path.read_text(),
        algorithm: str = settings.jwt.algorithm,
    ) -> str:
        to_encode = payload.copy()
        now = datetime.now(timezone.utc)
        expire = now + expire
        to_encode.update(
            exp=expire,
            iat=now,
        )
        encoded = jwt.encode(
            to_encode,
            private_key,
            algorithm=algorithm,
        )
        return encoded

    @staticmethod
    def decode_jwt(
        token: str | bytes,
        public_key: str = settings.jwt.public_key_path.read_text(),
        algorithm: str = settings.jwt.algorithm,
    ) -> dict:
        try:
            decoded = jwt.decode(
                token,
                public_key,
                algorithms=[algorithm],
            )
            return decoded
        except ExpiredSignatureError:
            raise

    @staticmethod
    def create_token(user_id: int, username: str, token_type: TokenType, expire: timedelta) -> str:
        payload = {"sub": f"user:{user_id}", "username": username, "type": token_type}
        return Token.encode_jwt(
            payload=payload,
            expire=expire,
        )

    @classmethod
    async def generate_tokens(cls, user_id: int, username: str):

        expire_access = timedelta(minutes=settings.jwt.access_token_expire_minutes)
        expire_refresh = timedelta(days=settings.jwt.refresh_token_expire_days)

        access_token = cls.create_token(user_id, username, token_type=TokenType.access, expire=expire_access)
        refresh_token = cls.create_token(user_id, username, token_type=TokenType.refresh, expire=expire_refresh)

        await RedisStorage.add_token(
            redis_client=redis_client, key=f"user:{user_id}", value=refresh_token, expire=expire_refresh
        )

        return access_token, refresh_token
