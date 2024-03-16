from fastapi import FastAPI

from src.api.ping import router as ping_router


app = FastAPI()

app.include_router(ping_router)
