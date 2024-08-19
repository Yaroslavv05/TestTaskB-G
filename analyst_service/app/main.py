from fastapi import FastAPI
from .tasks import fetch_data

app = FastAPI()

@app.on_event("startup")
def startup_event():
    # Запуск задач по расписанию
    fetch_data()
