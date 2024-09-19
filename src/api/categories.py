from fastapi import APIRouter, HTTPException, status
from fastapi_cache.decorator import cache

from models.categories import Category

from .dependencies import session
from .posts import Service

router = APIRouter(
    prefix="/categories",
)


@router.get("/{category}", summary="Получение постов по данной категории")
@cache(expire=30)
async def get_posts(
    category: Category,
    posts_service: Service,
    session: session,
):
    resp = await posts_service.get_posts(session, category=category)
    if not resp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Посты {category.value=} не найдены",
        )
    return {"response": resp}
