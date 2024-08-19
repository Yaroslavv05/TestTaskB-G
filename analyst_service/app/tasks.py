import redis
import requests
import time

r = redis.Redis(host='redis', port=6379, db=0)

def fetch_data():
    time.sleep(30)
    while True:
        users = requests.get("http://user-service:8001/users").json()
        posts = requests.get("http://post-service:8002/posts").json()

        analytics = {}
        for user in users:
            user_id = user['id']
            analytics[user_id] = sum(1 for post in posts if post['user_id'] == user_id)
            r.set(f"user:{user_id}:analytics", analytics[user_id])

        time.sleep(600)  # 10 минут
