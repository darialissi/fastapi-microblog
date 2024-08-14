from fastapi import APIRouter, HTTPException
from fastapi_cache.decorator import cache

from models.categories import Category
from api.dependencies import UOWDep
from services.posts import PostsService


router = APIRouter(
    prefix="/categories",
)


@router.get("/{category}") 
@cache(expire=30)
async def get_posts(category: Category,
    uow: UOWDep,
):
    resp = await PostsService().get_posts(uow, category=category)
    if not resp:
        raise HTTPException(status_code=404, detail="Посты не найдены")
    return {"response": resp}


