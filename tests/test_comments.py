from httpx import AsyncClient
import pytest
  
@pytest.mark.usefixtures("add_user", "add_post")   
class TestComments:
    @pytest.mark.parametrize(
        "method, endpoint, expected_status, data",
        [
            ("post", "/posts/1/comments", 200, {
                                    "author_id": 1,
                                    "body": "test comment",
                                    }),      
            ("post", "/posts/1/comments", 422, {
                                    "author_id": 0,
                                    "body": "test comment",
                                    }),      
            ("post", "/posts/5/comments", 400, {
                                    "author_id": 1,
                                    "body": "test comment",
                                    }),  
            ("patch", "/posts/1/comments/1", 200, {
                                        "body": "new comment",
                                    }), 
            ("patch", "/posts/1/comments/5", 400, {
                                        "body": "new comment",
                                    }),   
            ("get", "/posts/1/comments", 200, None),
            ("get", "/posts/5/comments", 404, None),
            ("get", "/posts/1/comments/1", 200, None),
            ("get", "/posts/1/comments/5", 404, None),
            ("delete", "/posts/1/comments/1", 200, None),
            ("delete", "/posts/1/comments/5", 400, None),
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