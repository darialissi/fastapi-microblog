from httpx import AsyncClient
import pytest


@pytest.mark.usefixtures("add_user")
class TestPosts:
    @pytest.mark.parametrize(
        "method, endpoint, expected_status, data",
        [ 
            ("post", "/posts", 201, {
                                    "user_id": 1,
                                    "title": "test title",
                                    "category": "development",
                                    "body": "test post",
                                    }),     
            ("post", "/posts", 400, {
                                    "user_id": 5, 
                                    "title": "test title",
                                    "category": "development",
                                    "body": "test post",
                                    }),  
            ("patch", "/posts/1", 200, {
                                        "title": "new title",
                                        "category": "development",
                                        "body": "test post",
                                    }),   
            ("patch", "/posts/5", 400, {
                                        "title": "new title",
                                        "category": "development",
                                        "body": "test post",
                                    }),  
            ("get", "/posts", 200, None),
            ("get", "/posts/1", 200, None),
            ("get", "/posts/5", 404, None),
            ("get", "/posts/categories/development", 200, None),
            ("get", "/posts/categories/design", 404, None),
            ("delete", "/posts/1", 200, None),
            ("delete", "/posts/5", 400, None),
        ],
    )
    async def test(self, ac: AsyncClient, method, endpoint, expected_status, data):       
        match method:
            case "post": 
                response = await ac.post(endpoint, json=data)
            case "get":
                response = await ac.get(endpoint)
            case "patch":
                response = await ac.patch(endpoint, json=data)
            case "delete":
                response = await ac.delete(endpoint)

        assert response.status_code == expected_status