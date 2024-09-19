import pytest
from fastapi import status
from httpx import AsyncClient


class TestComments:
    @pytest.mark.parametrize(
        "method, endpoint, expected_status, data",
        [
            (
                "post",
                "/posts/1/comments",
                status.HTTP_201_CREATED,
                {
                    "author_id": 1,
                    "body": "test comment",
                },
            ),
            (
                "post",
                "/posts/1/comments",
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                {
                    "author_id": 0,
                    "body": "test comment",
                },
            ),
            (
                "post",
                "/posts/5/comments",
                status.HTTP_400_BAD_REQUEST,
                {
                    "author_id": 1,
                    "body": "test comment",
                },
            ),
            (
                "patch",
                "/posts/1/comments/1",
                status.HTTP_200_OK,
                {
                    "body": "new comment",
                },
            ),
            (
                "patch",
                "/posts/1/comments/5",
                status.HTTP_400_BAD_REQUEST,
                {
                    "body": "new comment",
                },
            ),
            ("get", "/posts/1/comments", status.HTTP_200_OK, None),
            ("get", "/posts/5/comments", status.HTTP_404_NOT_FOUND, None),
            ("get", "/posts/1/comments/1", status.HTTP_200_OK, None),
            ("get", "/posts/1/comments/5", status.HTTP_404_NOT_FOUND, None),
            ("delete", "/posts/1/comments/1", status.HTTP_200_OK, None),
            ("delete", "/posts/1/comments/5", status.HTTP_400_BAD_REQUEST, None),
        ],
    )
    async def test(self, ac: AsyncClient, user_data, method, endpoint, expected_status, data):

        # auth user
        await ac.post("/auth/register", json=user_data)
        response = await ac.post("/auth/token", data=user_data)
        access_token = response.json()["access_token"]

        # create post
        await ac.post(
            "/posts",
            json={
                "user_id": 1,
                "title": "test title",
                "category": "development",
                "body": "test post",
            },
            headers={"Authorization": f"Bearer {access_token}"},
        )

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
