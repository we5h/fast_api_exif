import motor.motor_asyncio
from bson.objectid import ObjectId
from fastapi import FastAPI, HTTPException, Path, UploadFile

from config import settings
from schema import (ExifResponseModel, PhotoResponseModel, PhotoUploadModel,
                    list_of_photos, photo_dict)
from services import current_time, extract_exif, generate_filename

app = FastAPI()

client = None
db = None
photo_collection = None


@app.on_event("startup")
async def startup_event():

    """При запуске устанавливается соединение и переключение на коллекцию."""

    global client
    global db
    global photo_collection

    client = motor.motor_asyncio.AsyncIOMotorClient(settings.DATABASE_URL)

    db = client.photos

    photo_collection = db.photos_collection


@app.on_event("shutdown")
def shutdown_event():

    """Закрываем соединение при выключении."""

    global client
    client.close()


@app.get("/photos/", response_model=PhotoResponseModel)
async def get_photo():

    """Получить список фото."""

    photos = await list_of_photos(photo_collection)
    return {"amount": len(photos),
            "result": photos}


@app.get("/photos/{photo_id}", response_model=ExifResponseModel)
async def get_photo_by_id(photo_id: str = Path(pattern=r'^[a-f\d]{24}$')):

    """Получить фото по id(mongoID). Валидация regex. """

    result = 'Photo does not contain EXIF'
    document = await photo_collection.find_one(ObjectId(f'{photo_id}'))
    if not document:
        raise HTTPException(status_code=404, detail="Item not found")
    if document['exif']:
        result = document['exif']
    return ({'exif': result})


@app.post("/photos/",  response_model=PhotoUploadModel)
async def upload_photo(file: UploadFile,):

    """Загрузка фото. Валидация формата файла внутри generate_filename."""

    photo_data = {}

    photo_data['filename'] = generate_filename(file)
    photo_data['uploaded_at'] = current_time()

    data = await file.read()
    photo_data['file'] = data
    photo_data['exif'] = extract_exif(data)

    photo = await photo_collection.insert_one(photo_data)
    new_photo = await photo_collection.find_one({"_id": photo.inserted_id})
    return photo_dict(new_photo)
