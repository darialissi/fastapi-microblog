from fastapi import APIRouter, HTTPException
from fastapi_cache.decorator import cache

from models.categories import Category
from .posts import service
from .dependencies import session


router = APIRouter(
    prefix="/categories",
)

@router.get("/{category}") 
@cache(expire=30)
async def get_posts(category: Category,
    posts_service: service,
    session: session,
):
    resp = await posts_service.get_posts(session, category=category)
    if not resp:
        raise HTTPException(status_code=404, detail="Посты не найдены")
    return {"response": resp}


