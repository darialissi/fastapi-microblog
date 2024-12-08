import pytest
from fastapi import status
from httpx import AsyncClient

from schemas.comments import CommentSchemaAdd


class TestComments:
    @pytest.mark.parametrize(
        "method, endpoint, expected_status, data",
        [
            (
                "post",
                "/posts/1/comments",
                status.HTTP_201_CREATED,
                CommentSchemaAdd(body="test comment"),
            ),
            (
                "post",
                "/posts/5/comments",
                status.HTTP_400_BAD_REQUEST,
                CommentSchemaAdd(body="test comment"),
            ),
            (
                "patch",
                "/posts/1/comments/1",
                status.HTTP_200_OK,
                CommentSchemaAdd(body="test comment"),
            ),
            (
                "patch",
                "/posts/1/comments/5",
                status.HTTP_400_BAD_REQUEST,
                CommentSchemaAdd(body="test comment"),
            ),
            ("get", "/posts/1/comments", status.HTTP_200_OK, None),
            ("get", "/posts/5/comments", status.HTTP_404_NOT_FOUND, None),
            ("get", "/posts/1/comments/1", status.HTTP_200_OK, None),
            ("get", "/posts/1/comments/5", status.HTTP_404_NOT_FOUND, None),
            ("delete", "/posts/1/comments/1", status.HTTP_200_OK, None),
            ("delete", "/posts/1/comments/5", status.HTTP_400_BAD_REQUEST, None),
        ],
    )
    async def test(
        self,
        ac: AsyncClient,
        token_fixture: str,
        comment_fixture: None,
        method: str,
        endpoint: str,
        expected_status: status,
        data: CommentSchemaAdd,
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
