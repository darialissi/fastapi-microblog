import pytest
from fastapi import status
from httpx import AsyncClient

from models.categories import Category
from schemas.posts import PostSchemaAdd


class TestPosts:
    @pytest.mark.parametrize(
        "method, endpoint, expected_status, data",
        [
            (
                "post",
                "/posts",
                status.HTTP_201_CREATED,
                PostSchemaAdd(
                    title="test title",
                    category=Category.development,
                    body="test post",
                ),
            ),
            (
                "patch",
                "/posts/1",
                status.HTTP_200_OK,
                PostSchemaAdd(
                    title="new title",
                    category=Category.design,
                    body="test post",
                ),
            ),
            (
                "patch",
                "/posts/5",
                status.HTTP_400_BAD_REQUEST,
                PostSchemaAdd(
                    title="new title",
                    category=Category.management,
                    body="test post",
                ),
            ),
            ("get", "/posts", status.HTTP_200_OK, None),
            ("get", "/posts/1", status.HTTP_200_OK, None),
            ("get", "/posts/5", status.HTTP_404_NOT_FOUND, None),
            ("get", f"/posts/categories/{Category.design}", status.HTTP_200_OK, None),
            ("get", f"/posts/categories/{Category.marketing}", status.HTTP_404_NOT_FOUND, None),
            ("delete", "/posts/1", status.HTTP_200_OK, None),
            ("delete", "/posts/5", status.HTTP_400_BAD_REQUEST, None),
        ],
    )
    async def test(
        self,
        ac: AsyncClient,
        token_fixture: str,
        post_fixture: None,
        method: str,
        endpoint: str,
        expected_status: status,
        data: PostSchemaAdd,
    ):

        match method:
            case "post":
                response = await ac.post(
                    endpoint, data=data.model_dump_json(), headers={"Authorization": token_fixture}
                )
            case "get":
                response = await ac.get(endpoint, headers={"Authorization": token_fixture})
            case "patch":
                response = await ac.patch(
                    endpoint, data=data.model_dump_json(), headers={"Authorization": token_fixture}
                )
            case "delete":
                response = await ac.delete(endpoint, headers={"Authorization": token_fixture})

        assert response.status_code == expected_status
