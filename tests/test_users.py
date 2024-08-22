from httpx import AsyncClient
import pytest

from fastapi import status


class TestUsers:
    @pytest.mark.parametrize(
        "method, endpoint, expected_status, data",
        [
            ("post", "/auth/register", status.HTTP_201_CREATED, {"username": "user1", "password": "12345"}),    
            ("post", "/auth/register", status.HTTP_400_BAD_REQUEST, {"username": "user1", "password": "12345"}),   # existed username 
            ("patch", "/auth/account", status.HTTP_200_OK, {"username": "newname", "password": "12345"}), 
            ("get", "/auth/account", status.HTTP_200_OK, None),
            ("get", "/users", status.HTTP_200_OK, None),
            ("get", "/users/1", status.HTTP_200_OK, None),
            ("get", "/users/5", status.HTTP_404_NOT_FOUND, None), 
            ("delete", "/auth/account", status.HTTP_200_OK, None),
        ],
    )
    async def test(self, ac: AsyncClient, user_data, method, endpoint, expected_status, data):    

        await ac.post("/auth/register", json=user_data)

        not_auth = await ac.get("/auth/account")
        assert not_auth.status_code == status.HTTP_401_UNAUTHORIZED

        # auth user
        response = await ac.post("/auth/token", data=user_data)
        access_token = response.json()["access_token"]

        match method:
            case "post": 
                response = await ac.post(endpoint, json=data)
            case "get":
                response = await ac.get(endpoint, headers={"Authorization": f"Bearer {access_token}"})
            case "patch":
                response = await ac.patch(endpoint, json=data, headers={"Authorization": f"Bearer {access_token}"})
            case "delete":
                response = await ac.delete(endpoint, headers={"Authorization": f"Bearer {access_token}"})

        assert response.status_code == expected_status