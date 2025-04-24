import asyncio
from pydantic import ValidationError
from app.internal.config import RABBITMQ_URL, PHOTO_QUEUE_NAME
from app.internal.model.photo import Photo
from app.internal.consumer import photo_consumer
from app.pkg.logging.logger import log_error
from app.pkg.rabbitmq import RabbitmqClient


async def main():
    async with RabbitmqClient(RABBITMQ_URL, PHOTO_QUEUE_NAME) as client:
        async for photo_data in client.data_iter():
            try:
                photo = Photo.model_validate(photo_data)
                await photo_consumer.consume_photo(photo)
            except ValidationError:
                log_error("JSON Body cannot be processed as photo data")
            except Exception as e:
                log_error(str(e))


if __name__ == '__main__':
    asyncio.run(main())
