from datetime import datetime as dt
from secrets import token_hex

from exif import Image
from fastapi import HTTPException


def current_time() -> str:
    now = dt.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt_string


def generate_filename(file) -> str:
    allowed_formats = ('jpg', 'jpeg', 'gif', 'tiff', 'png')
    file_ext = file.filename.split('.').pop()
    if file_ext not in allowed_formats:
        raise HTTPException(status_code=415,
                            detail="Unable to upload this type of file.")
    file_name = token_hex(10) + '.' + file_ext
    return file_name


def extract_exif(file_data) -> list:
    exif = []
    image_file = Image(file_data)
    exif_params = image_file.list_all()
    for tag in exif_params:
        opened_tag = image_file.get(tag)
        if opened_tag:
            exif.append({tag: opened_tag})
    return exif
