from fastapi import FastAPI
import httpx
import redis
import asyncio
from sqlalchemy import create_engine, text

app = FastAPI()

DATABASE_URL = "postgresql://postgres:55dnBZ72x@db/TestTaskBG"
REDIS_HOST = "redis"
REDIS_PORT = 6379

engine = create_engine(DATABASE_URL)
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

async def fetch_users():
    async with httpx.AsyncClient() as client:
        response = await client.get('http://172.24.0.4:5000/users/')
        response.raise_for_status()
        return response.json()

async def fetch_posts():
    async with httpx.AsyncClient() as client:
        response = await client.get('http://172.25.0.4:8080/posts/')
        response.raise_for_status()
        return response.json()

async def analyze_data():
    users = await fetch_users()
    posts = await fetch_posts()

    user_post_count = {user['id']: 0 for user in users}
    for post in posts:
        if post['user_id'] in user_post_count:
            user_post_count[post['user_id']] += 1

    for user_id, post_count in user_post_count.items():
        r.set(user_id, post_count)

@app.on_event("startup")
async def startup_event():
    while True:
        await analyze_data()
        await asyncio.sleep(600)
