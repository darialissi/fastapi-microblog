from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_cache.decorator import cache

from models.categories import Category
from services.posts import PostsService

from .dependencies import UOW_db

router = APIRouter(
    prefix="/categories",
)


@router.get("/{category}", summary="Получение постов по данной категории")
@cache(expire=30)
async def get_posts(
    category: Category,
    db: UOW_db,
    service: PostsService = Depends(),
):
    resp = await service.get_posts(db, category=category)
    if not resp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Посты категории {category.value} не найдены",
        )
    return {"response": resp}
