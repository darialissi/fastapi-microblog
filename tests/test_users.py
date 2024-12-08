import pytest
from fastapi import status
from httpx import AsyncClient

from api.auth.schemas import TokenSchema
from schemas.users import UserSchemaAdd


class TestUsers:
    @pytest.mark.parametrize(
        "endpoint, expected_status",
        [
            ("/users", status.HTTP_200_OK),
            ("/users/1", status.HTTP_200_OK),
            ("/users/5", status.HTTP_404_NOT_FOUND),
        ],
    )
    async def test_users(self, ac: AsyncClient, register_fixture: None, endpoint: str, expected_status: status):

        response = await ac.get(endpoint)
        assert response.status_code == expected_status

    @pytest.mark.parametrize(
        "method, endpoint, expected_status, data",
        [
            ("get", "/auth/account", status.HTTP_200_OK, None),
            ("patch", "/auth/account", status.HTTP_200_OK, UserSchemaAdd(username="newname", password="12345")),
            ("delete", "/auth/account", status.HTTP_200_OK, None),
        ],
    )
    async def test_account(
        self, ac: AsyncClient, method: str, endpoint: str, expected_status: status, data: UserSchemaAdd
    ):

        # user for testing
        temp_user = UserSchemaAdd(username="temp_user", password="11111")
        register = await ac.post("/auth/register", data=temp_user.model_dump_json())
        assert register.status_code == status.HTTP_201_CREATED

        not_auth = await ac.get("/auth/account")
        assert not_auth.status_code == status.HTTP_401_UNAUTHORIZED

        # auth user
        response = await ac.post("/auth/token", data=temp_user.model_dump_json())
        assert response.json() is not None

        token = TokenSchema(**response.json())
        token_header = f"{token.token_type} {token.access_token}"

        match method:
            case "get":
                response = await ac.get(endpoint, headers={"Authorization": token_header})
            case "patch":
                response = await ac.patch(
                    endpoint, data=data.model_dump_json(), headers={"Authorization": token_header}
                )
            case "delete":
                response = await ac.delete(endpoint, headers={"Authorization": token_header})

        assert response.status_code == expected_status
