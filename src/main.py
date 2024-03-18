from fastapi import FastAPI

from src.api.ping import router as ping_router
from src.api.post import router as post_router
from .config import config

print(config.db_url)

app = FastAPI()

app.include_router(ping_router)
app.include_router(post_router)
