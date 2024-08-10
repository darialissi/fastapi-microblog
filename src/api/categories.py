from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from models.categories import Category
from .posts import service


router = APIRouter(
    prefix="/categories",
)

@router.get("/{category}") 
@cache(expire=30)
async def get_posts(category: Category,
    posts_service: service,
):
    posts = await posts_service.get_posts(category=category)
    return posts


