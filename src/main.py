import uvicorn
from fastapi import FastAPI

from api.routers import all_routers
from db.db import create_tables, drop_tables, init_cache

app = FastAPI(title="Microblog", on_startup=[create_tables, init_cache], on_shutdown=[drop_tables])

for router in all_routers:
    app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
    )
