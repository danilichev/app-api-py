from fastapi import FastAPI

from src.api import ping, post

from .config import config

print(config.db_url)

app = FastAPI()

app.include_router(ping.router)
app.include_router(post.router)
