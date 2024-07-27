from fastapi import HTTPException, UploadFile, status


def file_size_guard(max_size=5):
    def guard(file: UploadFile):
        if file.size > (max_size * 1024 * 1024):
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File size should be less than {max_size}MB",
            )
        return file

    return guard


def image_format_guard(image: UploadFile):
    file_format = image.filename.split(".")[-1]
    if file_format not in ["jpg", "jpeg", "png"]:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="File format should be jpeg, jpg or png",
        )
    return image


def image_guard(max_size=5):
    def guard(image: UploadFile):
        image = image_format_guard(image)
        image = file_size_guard(max_size)(image)
        return image

    return guard
