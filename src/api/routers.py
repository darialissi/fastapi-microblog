from api.posts import router as router_posts
from api.users import router as router_users
from api.categories import router as router_categories
from api.comments import router as router_comments

router_posts.include_router(router_categories)
router_posts.include_router(router_comments)

all_routers = [
    router_users,
    router_posts,
]