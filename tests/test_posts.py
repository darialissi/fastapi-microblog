from httpx import AsyncClient
import pytest

@pytest.fixture(scope="session")
async def add_post(ac: AsyncClient):
    await ac.post("/users", json={
        "user_id": 1,
        "title": "test title",
        "category": "development",
        "body": "test post",
    })

async def test_get_user(ac: AsyncClient):

    get_all = await ac.get("/posts")
    assert get_all.status_code == 200

    get_one = await ac.get("/posts/1")
    assert get_one.status_code == 200