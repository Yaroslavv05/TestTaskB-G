from fastapi import FastAPI
from app.api.v1 import post_router
from app.db.database import init_db

app = FastAPI()

init_db()

app.include_router(post_router.router)

