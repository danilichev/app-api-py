from fastapi import APIRouter


router = APIRouter()


@router.get("/ping")
async def root():
    return {"message": "pong"}
