from fastapi import FastAPI
from app.api.v1 import user_router
from app.db.database import init_db

app = FastAPI()

init_db()

# Регистрация маршрутов
app.include_router(user_router.router)

