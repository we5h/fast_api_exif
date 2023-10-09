from pydantic import BaseModel, Field


class PhotoUploadModel(BaseModel):
    id: str = Field(...)
    filename: str = Field(...)
    EXIF: list = Field(...)
    uploaded_at: str = Field(...)


class PhotoResponseModel(BaseModel):
    amount: int = Field(...)
    result: list = Field(...)


class ExifResponseModel(BaseModel):
    exif: list | str = Field(...)


def photo_dict(photo) -> dict:
    return {
        "id": str(photo["_id"]),
        "filename": photo["filename"],
        "EXIF": photo["exif"],
        "uploaded_at": photo["uploaded_at"]
    }


async def list_of_photos(collection) -> list:
    photos = []
    cursor = collection.find()
    for document in await cursor.to_list(length=100):
        del document['file']
        del document['exif']
        document['_id'] = str(document['_id'])
        photos.append(document)
    return photos
