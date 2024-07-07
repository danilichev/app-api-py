from fastapi import APIRouter


router = APIRouter(prefix="/ping")


@router.get("/")
async def ping_endpoint():
    return {"message": "pong"}
