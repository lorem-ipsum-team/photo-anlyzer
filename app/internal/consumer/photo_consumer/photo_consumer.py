from io import BytesIO
import asyncio
from PIL import Image
from app.internal.model.photo import Photo
from app.internal.service import downloader
from app.pkg.pytorch.facenet.facenet_processor import FacenetProcessor

processor = FacenetProcessor()


def process_photo(photo_bytes: bytes):
    img = Image.open(BytesIO(photo_bytes)).convert('RGB')
    return processor.process_image(img)


async def consume_photo(photo: Photo):
    image = await downloader.download_object(photo.image_url)

    loop = asyncio.get_event_loop()
    processed = await loop.run_in_executor(None, process_photo, image)
