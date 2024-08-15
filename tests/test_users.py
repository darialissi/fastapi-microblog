from httpx import AsyncClient
import pytest


class TestUsers:
    @pytest.mark.parametrize(
        "method, endpoint, expected_status, data",
        [
            ("post", "/users", 201, {"username": "user1", "password": "12345"}),    
            ("post", "/users", 400, {"username": "user1", "password": "12345"}),   # existed username  
            ("patch", "/users/1", 200, {"username": "newname", "password": "12345"}),    
            ("patch", "/users/5", 400, {"username": "newname", "password": "12345"}),  
            ("get", "/users", 200, None),
            ("get", "/users/1", 200, None),
            ("get", "/users/5", 404, None), 
            ("delete", "/users/1", 200, None),
            ("delete", "/users/5", 400, None),
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