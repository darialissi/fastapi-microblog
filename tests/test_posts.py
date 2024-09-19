import pytest
from fastapi import status
from httpx import AsyncClient


class TestPosts:
    @pytest.mark.parametrize(
        "method, endpoint, expected_status, data",
        [
            (
                "post",
                "/posts",
                status.HTTP_201_CREATED,
                {
                    "user_id": 1,
                    "title": "test title",
                    "category": "development",
                    "body": "test post",
                },
            ),
            (
                "post",
                "/posts",
                status.HTTP_400_BAD_REQUEST,
                {
                    "user_id": 5,
                    "title": "test title",
                    "category": "development",
                    "body": "test post",
                },
            ),
            (
                "patch",
                "/posts/1",
                status.HTTP_200_OK,
                {
                    "title": "new title",
                    "category": "development",
                    "body": "test post",
                },
            ),
            (
                "patch",
                "/posts/5",
                status.HTTP_400_BAD_REQUEST,
                {
                    "title": "new title",
                    "category": "development",
                    "body": "test post",
                },
            ),
            ("get", "/posts", status.HTTP_200_OK, None),
            ("get", "/posts/1", status.HTTP_200_OK, None),
            ("get", "/posts/5", status.HTTP_404_NOT_FOUND, None),
            ("get", "/posts/categories/development", status.HTTP_200_OK, None),
            ("get", "/posts/categories/design", status.HTTP_404_NOT_FOUND, None),
            ("delete", "/posts/1", status.HTTP_200_OK, None),
            ("delete", "/posts/5", status.HTTP_400_BAD_REQUEST, None),
        ],
    )
    async def test(self, ac: AsyncClient, user_data, method, endpoint, expected_status, data):

        # auth user
        await ac.post("/auth/register", json=user_data)
        response = await ac.post("/auth/token", data=user_data)
        access_token = response.json()["access_token"]

        match method:
            case "post":
                response = await ac.post(endpoint, json=data, headers={"Authorization": f"Bearer {access_token}"})
            case "get":
                response = await ac.get(endpoint)
            case "patch":
                response = await ac.patch(endpoint, json=data, headers={"Authorization": f"Bearer {access_token}"})
            case "delete":
                response = await ac.delete(endpoint, headers={"Authorization": f"Bearer {access_token}"})

        assert response.status_code == expected_status
