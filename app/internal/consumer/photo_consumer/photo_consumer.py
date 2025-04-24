from uuid import UUID
from io import BytesIO
import asyncio
from PIL import Image
from app.internal.entity.userdata import UserPhoto
from app.internal.model.photo import Photo
from app.internal.service import downloader
from app.internal.service.photo_repository import PhotoRepository
from app.pkg.asyncpg.database import async_session, AsyncSession
from app.pkg.pytorch.facenet.facenet_processor import FacenetProcessor

processor = FacenetProcessor()


def process_photo(photo_bytes: bytes):
    img = Image.open(BytesIO(photo_bytes)).convert('RGB')
    return processor.process_image(img)


async def consume_photo(photo: Photo):
    image = await downloader.download_object(photo.image_url)

    loop = asyncio.get_event_loop()
    processed = await loop.run_in_executor(None, process_photo, image)
    photo_data = processed[0].tolist()

    async with async_session() as session:
        session: AsyncSession
        photos = PhotoRepository()
        uuid = UUID(photo.user_id)

        item = await photos.get_by_id(uuid, session)

        if item is None:
            item = UserPhoto(
                id=uuid,
                data=photo_data
            )

            session.add(item)

        item.data = photo_data
        await session.commit()
