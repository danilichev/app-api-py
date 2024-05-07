from fastapi import APIRouter, UploadFile

from src.utils.files import write_temp_file


router = APIRouter()


@router.post("/file")
async def upload_file_endpoint(
    file: UploadFile,
):
    await write_temp_file(file)
    return {"filename": file.filename}
