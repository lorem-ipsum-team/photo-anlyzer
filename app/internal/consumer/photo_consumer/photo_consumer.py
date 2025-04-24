import base64
from io import BytesIO
import asyncio
from PIL import Image
from app.internal.model.photo import Photo
from app.pkg.pytorch.facenet.facenet_processor import FacenetProcessor

processor = FacenetProcessor()


def process_photo(photo: Photo):
    image = base64.b64decode(photo.image_base64)
    img = Image.open(BytesIO(image)).convert('RGB')
    return processor.process_image(img)


async def consume_photo(photo: Photo):
    loop = asyncio.get_event_loop()
    processed = await loop.run_in_executor(None, process_photo, photo)
