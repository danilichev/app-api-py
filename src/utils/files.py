from fastapi import UploadFile
from typing import List, Optional
import aiofiles
import csv
import os
import uuid

from src.config import config


async def write_temp_file(file: UploadFile, file_name: Optional[str] = None):
    file_ext = f".{file.filename.split('.')[-1]}"
    file_path = f"{config.temp_dir}/{str(uuid.uuid4()) + file_ext if file_name is None else file_name}"
    async with aiofiles.open(file_path, mode="wb+") as f:
        contents = await file.read()
        await f.write(contents)
        return file_path


def remove_file(file_path: str):
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        print("The file does not exist")


def remove_files(file_pathes: List[str]):
    for file_path in file_pathes:
        remove_file(file_path)


async def read_file(file_path: str, mode="rb") -> bytes:
    print(f"Reading file {file_path}")
    async with aiofiles.open(file_path, mode) as file:
        return await file.read()


async def read_csv_file(file_path: str):
    data = await read_file(file_path, "r")
    reader = csv.reader(data.splitlines())
    return [row for row in reader]
