from httpx import AsyncClient
import pytest

@pytest.fixture(scope="session")
async def add_user(ac: AsyncClient):
    await ac.post("/users", json={
        "username": "test user",
        "password": "12345",
    })


async def test_get_user(ac: AsyncClient):

    get_all = await ac.get("/users")
    assert get_all.status_code == 200

    get_one = await ac.get("/users/1")
    assert get_one.status_code == 200