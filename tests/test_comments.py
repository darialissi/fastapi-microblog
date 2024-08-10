from httpx import AsyncClient
import pytest

@pytest.fixture(scope="module")
async def add_comment(ac: AsyncClient):
    response = await ac.post("/posts/1/comments", json={
        "author_id": 1,
        "body": "test comment",
    })

async def test_get_comment(ac: AsyncClient):

    get_all = await ac.get("/posts/1/comments")
    assert get_all.status_code == 200

    get_one = await ac.get("/posts/1/comments/1")
    assert get_one.status_code == 200